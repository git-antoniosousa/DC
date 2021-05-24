import datetime
from odoo import models, api, fields
import pytz

class MapaReport(models.AbstractModel):
    _name = 'report.gestao_equipas.report_reg_presencas_evento_generate'

    def get_evento(self, evento_id):
        return self.env['ges.evento_desportivo'].browse(evento_id)

    def get_info_evento(self, evento_desportivo):
        tz_local = pytz.timezone(self.env.user.partner_id.tz or 'UTC')
        start_naive = fields.Datetime.from_string(evento.start)
        stop_naive = fields.Datetime.from_string(evento.stop)

        inicio = start_naive + timedelta(seconds=tz_local.utcoffset(start_naive).seconds)
        fim = stop_naive + timedelta(seconds=tz_local.utcoffset(stop_naive).seconds)

        dia = start.strftime('%d/%m/%Y')
        inicio = start.strftime('%Hh%M')
        fim = stop.strftime('%Hh%M')

        if type(evento_desportivo.local.descricao) == bool:
            local = ""
        else:
            local = evento_desportivo.local.descricao

        info = '''
            <tr>
                <td>
                    <b>Dia: </b>''' + dia + '''
                </td>
            <tr>
                <td>
                    <b>Horário: </b>''' + inicio + ''' - ''' + fim + ''' (''' + str(evento_desportivo.duracao) + ''' minutos)
                </td>
            </tr>
            <tr>
                <td>
                    <b>Local: </b>''' + str(local) + ''')
                </td>
            </tr>
            <tr>
                <td>
                    <b>Escalão: </b>''' + str(evento_desportivo.escalao.designacao) + '''
                </td>
            </tr>
            <tr>
                <td>
                    <b>Treinador: </b>''' + str(evento_desportivo.treinador.name) + '''
                </td>
            </tr>
        '''
        return info

    def get_table_row(self, linha_convocatoria):
        if linha_convocatoria.presente:
            presente = '<td>Sim</td>'
            if linha_convocatoria.atrasado:
                atrasado = '<td style="background-color: #ffcfb2;>Sim</td>'
            else:
                atrasado = '<td>Não</td>'
        else:
            presente = '<td style="background-color: #ffb2b2;">Não</td>'
            atrasado = '<td>-</td>'

        row = '''
            <td>''' + linha_convocatoria.atleta.name + '''</td>
            ''' + presente + '''
            ''' + atrasado + '''
        '''
        return row

    @api.model
    def get_report_values(self, doc_ids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        evento_desportivo = self.get_evento(data['evento_id'])

        doc_args = {
            'doc_ids': doc_ids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            'evento': evento_desportivo,
            'linhas_presenca': evento_desportivo.presencas,
            'get_info_evento': self.get_info_evento,
            'get_table_row': self.get_table_row,
        }
        return doc_args
