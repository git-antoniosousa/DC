# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Socio(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Socio'
    _order = 'name'

    numero_socio = fields.Integer(string='Número de sócio')
    membro_gratis = fields.Boolean(string='Membro grátis', default=True)
    subscricao = fields.Many2one('ges.subscricao', string='Subscrição')
    faturas = fields.One2many('account.invoice', 'partner_id', 'Faturas')

    _sql_constraints = [('numero_socio_uniq',
                         'UNIQUE (numero_socio)',
                         'Não pode haver dois sócios com o mesmo número')]

    @api.one
    def gen_fatura(self):
        invoice = self.env['account.invoice'].create({
            'name': self.subscricao.descricao,
            'date_invoice': fields.date.today(),
            'account_id': self.env['account.account'].search([('code', '=', '211100')]).id,
            'payment_term_id': self.subscricao.payment_term.id,
            'partner_id': self.id,
        })
        self.env['account.invoice.line'].create({
            'invoice_id': invoice.id,
            'name': self.subscricao.product.name,
            'account_id': self.env['account.account'].search([('code', '=', '211100')]).id,
            'product_id': self.subscricao.product.id,
            'price_unit': self.subscricao.montante,
        })
        invoice.action_invoice_open()

    @api.model
    def create(self, vals):
        vals['numero_socio'] = self.env['ir.sequence'].next_by_code('ges.socio_seq')
        return super(Socio, self).create(vals)


