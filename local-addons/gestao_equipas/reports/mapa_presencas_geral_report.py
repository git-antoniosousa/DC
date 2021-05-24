import datetime
from datetime import datetime, timedelta
from odoo import models, api, fields
import pytz

class MapaReport(models.AbstractModel):
    _name = 'report.gestao_equipas.report_mapa_presencas_generate'

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

    def get_atletas(self):
        atletas = []
        for atleta in self.env['ges.atleta'].search([]):
            atletas.append(atleta)
        return atletas

    def model_evento(self, evento):
        if 'treino' in str(evento):
            return 'Treino'
        else:
            return 'Jogo'

    def get_heading_evento(self, evento):
        model = self.model_evento(evento)
        tz_local = pytz.timezone(self.env.user.partner_id.tz or 'UTC')
        start_naive = fields.Datetime.from_string(evento.start)
        stop_naive = fields.Datetime.from_string(evento.stop)

        start = start_naive + timedelta(seconds=tz_local.utcoffset(start_naive).seconds)
        stop = stop_naive + timedelta(seconds=tz_local.utcoffset(stop_naive).seconds)

        data = start.strftime('%d/%m')
        start = start.strftime('%Hh%M')
        stop = stop.strftime('%Hh%M')

        heading = '''
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
        return heading

    def get_heading(self, eventos):
        heading = '<th rowspan="2"></th>'
        for evento in eventos:
            heading += '''
                <th class="text-center">''' + self.get_heading_evento(evento) + '''</th>
            '''
        heading += '''
            <th rowspan="2" class="text-center">C</th>
            <th rowspan="2" class="text-center">I</th>
            <th rowspan="2" class="text-center">F</th>
            <th rowspan="2" class="text-center">A</th>
        '''
        return heading

    def get_row_escalao(self, eventos):
        row = ''
        for evento in eventos:
            row += '''
                <td class="text-center"><small>''' + evento.escalao.designacao + '''</small></td>
            '''
        return row

    def get_row_atleta(self, atleta, eventos):
        n_convocatorias = 0
        n_indisponibilidades = 0
        n_faltas = 0
        n_atrasos = 0

        row = '''
            <th>''' + atleta.name + '''</th>
        '''
        for evento in eventos:
            if atleta.id not in evento.atletas.ids:
                row += '''
                    <td></td>
                '''
            else:
                convocatorias = list(filter(lambda line: line.atleta.id == atleta.id, evento.convocatorias))
                if len(convocatorias) > 0:
                    convocatoria = convocatorias[0]
                    symbol = ''
                    style = ''
                    n_convocatorias += 1
                    if convocatoria.disponivel:
                        presencas = list(filter(lambda line: line.atleta.id == atleta.id, evento.presencas))
                        if len(presencas) > 0:
                            presenca = presencas[0]
                            if presenca.presente:
                                symbol += 'P'
                                if presenca.atrasado:
                                    n_atrasos += 1
                                    symbol += 'A'
                                    style = 'style="background-color: #ffcfb2;"'
                            else:
                                n_faltas += 1
                                symbol += 'F'
                                style = 'style="background-color: #ffb2b2;"'
                    else:
                        n_indisponibilidades += 1
                        style = 'style="background-color: #fff2b2;"'
                        symbol += 'I'
                row += '''
                    <td class="text-center" ''' + style + '''>''' + symbol + '''</td>
                '''

        if n_convocatorias == 0:
            return ''

        row += '''
            <td class="text-center">''' + str(n_convocatorias) + '''</td>
            <td class="text-center">''' + str(n_indisponibilidades) + '''</td>
            <td class="text-center">''' + str(n_faltas) + '''</td>
            <td class="text-center">''' + str(n_atrasos) + '''</td>
        '''

        return row

    @api.model
    def get_report_values(self, doc_ids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        atletas = self.get_atletas()
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
            'atletas': atletas,
            'get_heading': self.get_heading,
            'get_row_escalao': self.get_row_escalao,
            'get_row_atleta': self.get_row_atleta,
        }
        return doc_args
