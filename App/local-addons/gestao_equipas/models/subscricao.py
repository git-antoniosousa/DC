# -*- coding: utf-8 -*-


from odoo import models, fields, api


class Subscricao(models.Model):
    _name = 'ges.subscricao'
    _description = 'Subscrição'
    _order = 'descricao'
    _rec_name = 'descricao'

    descricao = fields.Char(string="Descricao", required=True)
    periodicidade = fields.Selection([('semamal', 'Semanal'),
                                      ('mensal', 'Mensal'),
                                      ('trimestral', 'Trimestral'),
                                      ('semestral', 'Semestral'),
                                      ('anual', 'Anual')], required=True)
    montante = fields.Float(string='Montante',
                            default=0,
                            required=True)
    currency_id = fields.Many2one('res.currency',
                                  string='Moeda',
                                  default=lambda self:
                                  self.env.user.company_id.currency_id)
    payment_term = fields.Many2one('account.payment.term', "Termo de pagamento", required=True)
    socios = fields.One2many('res.partner', 'subscricao', string="Sócios")
    product = fields.Many2one('product.product', "Produto")

    @api.model
    def create(self, values):
        product_obj = self.env['product.product']
        values['product'] = product_obj.create({
            'name': values['descricao'],
            'list_price': values['montante'],
        }).id
        return super(Subscricao, self).create(values)
