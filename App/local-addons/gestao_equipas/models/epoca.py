# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class Epoca(models.Model):
    _name = 'ges.epoca'
    _description = 'Época'
    _order = 'data_inicio DESC'

    name = fields.Char('Nome da época', required=True)
    data_inicio = fields.Date('Data de início', required=True)
    data_fim = fields.Date('Data de fim', required=True)
    atual = fields.Boolean('Época atual', default=False)
    competicoes = fields.One2many(comodel_name="ges.competicao",
                                  inverse_name="epoca",
                                  string="Competições")

    show_button = fields.Boolean(compute='_show_button')

    @api.onchange('atual', 'data_fim')
    def _show_button(self):
        today = date.today()
        for rec in self:
            if type(rec.data_fim) == bool:
                rec.show_button = False
            elif (fields.Date.from_string(rec.data_fim) > today) and not rec.atual:
                rec.show_button = True
            else:
                rec.show_button = False

    def epoca_atual(self):
        epoca_atual = self.env['ges.epoca'].search([('atual', '=', True)])
        if len(epoca_atual) == 1:
            epoca_atual[0].write({
                'atual': False
            })
        self.write({
            'atual': True
        })

        atletas = self.env['ges.atleta'].search([])
        for atleta in atletas:
            atleta._compute_escalao()

    @api.onchange('data_inicio')
    def _change_data_inicio(self):
        for rec in self:
            rec.data_fim = rec.data_inicio

    @api.onchange('data_inicio', 'data_fim')
    def actualiza_data(self):
        for registo in self:
            datetime_inicio = fields.Date.from_string(registo.data_inicio)
            datetime_fim = fields.Date.from_string(registo.data_fim)

            if (datetime_inicio is not None) and (datetime_fim is not None):
                nome_epoca = 'Época {}/{}'.format(
                    str(datetime_inicio.year)[-2:],
                    str(datetime_fim.year)[-2:])
                registo.name = nome_epoca
