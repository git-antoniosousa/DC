import datetime
import time
from odoo import models, api, fields


class HorarioReportAtleta(models.AbstractModel):
    _name = 'report.gestao_equipas.report_horario_seccionista_generate'
    _inherit = ['report.gestao_equipas.report_horario_generate']

    def get_seccionista(self, seccionista_id):
        seccionista = self.env['ges.seccionista'].browse(seccionista_id)
        return seccionista

    def gen_box(self, evento, first_hour):
        (position, height) = self.get_position_height(evento, first_hour)
        model = str(evento)
        if 'treino' in model:
            model = 'Treino'
        else:
            model = 'Jogo'

        if type(evento.local.descricao) == bool:
            local = ""
        else:
            local = evento.local.descricao

        box = '''
            <td style="width: 100%; padding-top: 2px; position: absolute; overflow: hidden; ''' + position + height + '''">
                <div>
                    <small>''' + self.format_hour(evento.start) + '''</small> 
                        - 
                    <small> ''' + self.format_hour(evento.stop) + '''</small>
                </div>
                <div>
                    <b> ''' + model + '''</b>
                </div>
                <div>
                    <span> ''' + local + '''</span>
                </div>
                <div>
                    <small> ''' + evento.escalao.designacao + '''</small>
                </div>
            </td>
        '''
        return box

    @api.model
    def get_report_values(self, doc_ids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        seccionista = self.get_seccionista(data['seccionista'][0])
        treinos = self.get_treinos(data['treinos_ids'])
        jogos = self.get_jogos(data['jogos_ids'])
        eventos = treinos + jogos
        first_hour = self.get_first_hour(eventos)

        doc_args = {
            'doc_ids': doc_ids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            'time': time,
            'seccionista': seccionista,
            'eventos': eventos,
            'first_hour': first_hour,
            'get_heading': self.get_heading,
            'get_eventos_of_day': self.get_eventos_of_day,
            'format_hour': self.format_hour,
            'gen_box': self.gen_box,
        }
        return doc_args
