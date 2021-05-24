from datetime import datetime, date
import calendar
from odoo import models, fields, api


class HorarioReport(models.TransientModel):
    _name = 'presencas.report'
    _description = 'Gerar mapa de presenças'

    mapa_de = fields.Selection([('atleta', 'Atleta'), ('escalao', 'Escalão')], 'Mapa de',
                               default='atleta', required=True)
    mes = fields.Selection([('1', 'Janeiro'),
                            ('2', 'Fevereiro'),
                            ('3', 'Março'),
                            ('4', 'Abril'),
                            ('5', 'Maio'),
                            ('6', 'Junho'),
                            ('7', 'Julho'),
                            ('8', 'Agosto'),
                            ('9', 'Setembro'),
                            ('10', 'Outubro'),
                            ('11', 'Novembro'),
                            ('12', 'Dezembro')], 'Mês', required=True, default=str(date.today().month))
    ano = fields.Char('Ano', default=str(date.today().year), required=True)
    atleta = fields.Many2one('ges.atleta', 'Atleta')
    escalao = fields.Many2one('ges.escalao', 'Escalão')

    @api.multi
    def gen_presencas_report_atleta(self):
        data = self.read(
            ['atleta', 'mes', 'ano']
        )[0]
        ano = int(data['ano'])
        mes = int(data['mes'])
        timerange = calendar.monthrange(ano, mes)
        data_inicio = date(ano, mes, 1)
        data_fim = date(ano, mes, timerange[1])
        treinos = self.env['ges.treino'].search(
            [('atletas', 'in', data['atleta'][0]),
             ('state', '!=', 'aberto'),
             ('start', '>=', fields.Date.to_string(data_inicio)),
             ('stop', '<=', fields.Date.to_string(data_fim))],
            order='start DESC'
        )
        jogos = self.env['ges.jogo'].search(
            [('atletas', 'in', data['atleta'][0]),
             ('state', '!=', 'aberto'),
             ('start', '>=', fields.Date.to_string(data_inicio)),
             ('stop', '<=', fields.Date.to_string(data_fim))],
            order='start DESC'
        )
        if len(treinos.ids) == 0 and len(jogos.ids) == 0:
            raise models.ValidationError(
                'Não existem treinos e jogos registados no período especificado.')
        data.update({'data_inicio': data_inicio,
                     'data_fim': data_fim,
                     'treinos_ids': treinos.ids,
                     'jogos_ids': jogos.ids})
        return self.env.ref('gestao_equipas.report_presencas_atleta_generate').report_action(self, data=data)

    @api.multi
    def gen_presencas_report(self):
        data = self.read(
            ['atleta', 'mapa_de', 'escalao', 'mes', 'ano']
        )[0]
        ano = int(data['ano'])
        mes = int(data['mes'])
        timerange = calendar.monthrange(ano, mes)
        data_inicio = date(ano, mes, 1)
        data_fim = date(ano, mes, timerange[1])

        if data['mapa_de'] == 'escalao':
            treinos = self.env['ges.treino'].search(
                [('escalao', '=', data['escalao'][0]),
                 ('state', '!=', 'aberto'),
                 ('start', '>=', fields.Date.to_string(data_inicio)),
                 ('stop', '<=', fields.Date.to_string(data_fim))],
                order='start DESC'
            )
            jogos = self.env['ges.jogo'].search(
                [('escalao', '=', data['escalao'][0]),
                 ('state', '!=', 'aberto'),
                 ('start', '>=', fields.Date.to_string(data_inicio)),
                 ('stop', '<=', fields.Date.to_string(data_fim))],
                order='start DESC'
            )
            if len(treinos.ids) == 0 and len(jogos.ids) == 0:
                raise models.ValidationError(
                    'Não existem treinos e jogos registados no período especificado.')
            data.update({'data_inicio': data_inicio,
                         'data_fim': data_fim,
                         'treinos_ids': treinos.ids,
                         'jogos_ids': jogos.ids})
            return self.env.ref('gestao_equipas.report_presencas_geral_generate').report_action(self, data=data)
        elif data['mapa_de'] == 'atleta':
            treinos = self.env['ges.treino'].search(
                [('atletas', 'in', data['atleta'][0]),
                 ('state', '!=', 'aberto'),
                 ('start', '>=', fields.Date.to_string(data_inicio)),
                 ('stop', '<=', fields.Date.to_string(data_fim))],
                order='start DESC'
            )
            jogos = self.env['ges.jogo'].search(
                [('atletas', 'in', data['atleta'][0]),
                 ('state', '!=', 'aberto'),
                 ('start', '>=', fields.Date.to_string(data_inicio)),
                 ('stop', '<=', fields.Date.to_string(data_fim))],
                order='start DESC'
            )
            if len(treinos.ids) == 0 and len(jogos.ids) == 0:
                raise models.ValidationError(
                    'Não existem treinos e jogos registados no período especificado.')
            data.update({'data_inicio': data_inicio,
                         'data_fim': data_fim,
                         'treinos_ids': treinos.ids,
                         'jogos_ids': jogos.ids})
            return self.env.ref('gestao_equipas.report_presencas_atleta_generate').report_action(self, data=data)
