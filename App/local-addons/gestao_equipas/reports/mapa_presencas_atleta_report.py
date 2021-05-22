import datetime
from datetime import timedelta, timezone
from odoo import models, api, fields
import pytz

class MapaReport(models.AbstractModel):
    _name = 'report.gestao_equipas.report_mapa_presencas_atleta_generate'

    n_convocatorias = 0
    n_indisponibilidades = 0
    n_faltas = 0
    n_atrasos = 0

    def get_treinos(self, treinos_ids):
        treinos = []
        for treino in self.env['ges.treino'].browse(treinos_ids):
            treinos.append(treino)
        return treinos

    def get_jogos(self, jogos_ids):
        jogos = []
        for jogo in self.env['ges.jogo'].browse(jogos_ids):
            jogos.append(jogo)
        return jogos

    def model_evento(self, evento):
        if 'treino' in str(evento):
            return 'Treino'
        else:
            return 'Jogo'


    def get_treinador_info(self, evento_desportivo):
        ttable =""
        tnames = list()
        for treinador in evento_desportivo.treinador:
            tnames.append(treinador.name)

        ttable = ", ".join(tnames)
        return ttable


    def get_cell_evento(self, evento):
        model = self.model_evento(evento)
        tz_local = pytz.timezone(self.env.user.partner_id.tz or 'UTC')
        start_naive = fields.Datetime.from_string(evento.start)
        stop_naive = fields.Datetime.from_string(evento.stop)

        start = start_naive + timedelta(seconds = tz_local.utcoffset(start_naive).seconds)
        stop = stop_naive + timedelta(seconds=tz_local.utcoffset(stop_naive).seconds)

        data = start.strftime('%d/%m')
        start = start.strftime('%Hh%M')
        stop = stop.strftime('%Hh%M')
        cell = '''
            <div>
                <span><b>''' + data + '''</b></span>
            </div>
            <div>
                <small><b>''' + start + '-' + stop + '''</b></small>
            </div>
            <div>
                <small>''' + model + '''</small>
            </div>
        '''
        return cell

    def get_row_evento(self, atleta, evento):
        row = ''
        convocatorias = list(filter(lambda line: line.atleta.id == atleta.id, evento.convocatorias))
        symbol = ''
        style = ''
        if len(convocatorias) > 0:
            convocatoria = convocatorias[0]
            self.n_convocatorias += 1

            if type(evento.local.descricao) == bool:
                local = ""
            else:
                local = evento.local.descricao

            row += '''
                <td>''' + self.get_cell_evento(evento) + '''</td>
                <td>''' + evento.escalao.designacao + '''</td>
                <td> ''' + str(self.get_treinador_info(evento))  + '''</td>
                <td>''' + local + '''</td>
            '''
            # evento.treinador.name
            if convocatoria.disponivel:
                presencas = list(filter(lambda line: line.atleta.id == atleta.id, evento.presencas))
                if len(presencas) > 0:
                    presenca = presencas[0]
                    if presenca.presente:
                        symbol += 'P'
                        if presenca.atrasado:
                            self.n_atrasos += 1
                            symbol += 'A'
                            style = 'style="background-color: #ffcfb2;"'
                    else:
                        self.n_faltas += 1
                        symbol += 'F'
                        style = 'style="background-color: #ffb2b2;"'
            else:
                self.n_indisponibilidades += 1
                style = 'style="background-color: #fff2b2;"'
                symbol += 'I'
            row += '''
                <td class="text-center" ''' + style + '''>''' + symbol + '''</td>
            '''
        return row

    def get_resumo(self):
        row = '''
            <tr>
                <th>Número de convocatórias</th>
                <td>''' + str(self.n_convocatorias) + '''</td>
            </tr>
            <tr>
                <th>Número de indisponibilidades</th>
                <td>''' + str(self.n_indisponibilidades) + '''</td>
            </tr>
            <tr>
                <th>Número de faltas</th>
                <td>''' + str(self.n_faltas) + '''</td>
            </tr>
            <tr>
                <th>Número de atrasos</th>
                <td>''' + str(self.n_atrasos) + '''</td>
            </tr>
        '''
        return row

    @api.model
    def get_report_values(self, doc_ids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        atleta = self.env['ges.atleta'].browse(data['atleta'][0])
        treinos = self.get_treinos(data['treinos_ids'])
        jogos = self.get_jogos(data['jogos_ids'])
        eventos = treinos + jogos
        eventos = sorted(eventos, key=lambda evento: fields.Datetime.from_string(evento.start))

        doc_args = {
            'doc_ids': doc_ids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            'eventos': eventos,
            'atleta': atleta,
            'get_row_evento': self.get_row_evento,
            'get_resumo': self.get_resumo,
        }
        return doc_args
