# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import timedelta, date, datetime


class Pagamento(models.Model):
    _name = 'ges.pagamento'
    _description = 'Pagamento'
    _order = 'data_limite'
    _rec_name = 'descricao'

    descricao = fields.Char(string='Descrição')
    data_emissao = fields.Date(string='Data Emissão')
    data_limite = fields.Date(string='Data Limite')
    montante = fields.Float(digits=(5, 2), string='Montante')
    currency_id = fields.Many2one('res.currency', string='Moeda',
                                  default=lambda self:
                                  self.env.user.company_id.currency_id)
    socio_id = fields.Many2one(comodel_name='res.partner', string='Sócio')
    subscricao_id = fields.Many2one(comodel_name='ges.subscricao',
                                    string='Referente a')
    regularizado = fields.Boolean(string="Regularizado?",
                                  compute='check_estado')

    @api.onchange('data_limite')
    def check_estado(self):
        datetime_limite = fields.Date.from_string(self.data_limite)
        if datetime_limite is not None:
            if datetime.now().date() > datetime_limite:
                self.regularizado = False
            else:
                self.regularizado = True
