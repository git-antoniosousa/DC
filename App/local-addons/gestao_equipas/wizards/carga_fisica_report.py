# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class CargaFisicaReport(models.TransientModel):
    _name = 'carga_fisica.report'
    _description = 'Gerar report de carga física'

    data_inicio = fields.Date('Data de início', required=True,
                              default=(datetime.today() - relativedelta(
                                  days=datetime.date(datetime.today()).weekday()
                              )))

    data_fim = fields.Date('Data de fim', required=True,
                           default=(datetime.today() + relativedelta(
                               days=6 - datetime.date(
                                   datetime.today()).weekday()
                           )))

    atleta = fields.Many2one(comodel_name='ges.atleta',
                             string='Atleta')

    @api.multi
    @api.constrains('data_inicio', 'data_fim')
    def _check_dates(self):
        for r in self:
            start_date = fields.Date.from_string(r.data_inicio)
            end_date = fields.Date.from_string(r.data_fim)
            if end_date < start_date:
                raise models.ValidationError(
                    'A data de fim não poderá ser anterior à data de início')

    @api.multi
    def gen_carga_fisica_report(self):
        data = self.read(['data_inicio', 'data_fim', 'atleta'])[0]

        treinos = self.env['ges.treino'].search(
            [('atletas', 'in', data['atleta'][0]),
             ('start', '>=', data['data_inicio']),
             ('stop', '<=', data['data_fim'])],
            order='start DESC'
        )

        jogos = self.env['ges.jogo'].search(
            [('atletas', 'in', data['atleta'][0]),
             ('start', '>=', data['data_inicio']),
             ('stop', '<=', data['data_fim'])],
            order='start DESC'
        )

        n_treinos, n_jogos = len(treinos), len(jogos)

        data.update({'n_treinos': n_treinos,
                     'n_jogos': n_jogos,
                     'treinos_ids': treinos.ids,
                     'jogos_ids': jogos.ids})

        return self.env.ref('gestao_equipas.report_carga_fisica_generate') \
            .report_action(self, data=data)
