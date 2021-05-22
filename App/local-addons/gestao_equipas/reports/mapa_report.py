from datetime import datetime
from datetime import timedelta, timezone
from odoo import models, api, fields
import pytz


class MapaReport(models.AbstractModel):
    _name = 'report.gestao_equipas.report_mapa_treinos_jogos_generate'

    current_escalao = ''

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

    def get_atletas(self, eventos_desportivos):
        atletas = []
        for evento in eventos_desportivos:
            for atleta in evento.atletas:
                if atleta not in atletas:
                    atletas.append(atleta)
        atletas = sorted(atletas, key=lambda atleta: atleta.escalao.id)
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
                <th class="text-center" valign="top" >''' + self.get_heading_evento(evento) + '''</th>
            '''
        return heading

    def get_row_escalao(self, eventos):
        row = ''
        for evento in eventos:
            row += '''
                <td class="text-center"><small>''' + evento.escalao.designacao + '''</small></td>
            '''
        return row

    def get_symbol_style(self, atleta, evento):
        if atleta.id not in evento.atletas.ids:
            return ('', '')
        res = list(filter(lambda line: line.atleta.id == atleta.id, evento.convocatorias))
        if len(res) > 0:
            line = res[0]
            if line.disponivel:
                return ('C', '')
            else:
                return ('I', 'style="background-color: #fff2b2;"')

    def get_row_atleta(self, atleta, eventos):
        if (self.current_escalao != atleta.escalao.designacao):
            self.current_escalao = atleta.escalao.designacao
            row = '''
                    <th colspan="''' + str(
                len(eventos) + 1) + '''" style="text-align: center;">''' + self.current_escalao + ''' </th>
                </tr>
                <tr>
            '''
        else:
            row = ''
        row += '''
            <th>''' + atleta.name + '''</th>
        '''
        for evento in eventos:
            res = self.get_symbol_style(atleta, evento)
            row += '''
                <td class="text-center" ''' + res[1] + '''>''' + res[0] + '''</td>
            '''
        return row

    @api.model
    def get_report_values(self, doc_ids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        treinos = self.get_treinos(data['treinos_ids'])
        jogos = self.get_jogos(data['jogos_ids'])
        eventos = treinos + jogos
        eventos = sorted(eventos, key=lambda evento: fields.Datetime.from_string(evento.start))
        atletas = self.get_atletas(eventos)

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
