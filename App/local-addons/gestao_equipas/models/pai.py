# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta, date


class Pai(models.Model):
    _name = 'ges.pai'
    _inherits = {'res.users': 'user_id'}
    _description = 'Pai'
    _order = 'name'
    _rec_name = 'name'

    user_id = fields.Many2one('res.users', ondelete='restrict', required=True)
    filhos = fields.Many2many('ges.atleta', string='Filhos')
    utilizador_existe = fields.Selection([('sim', 'Sim'),
                                          ('nao', 'Não')],
                                         'Já registado como outro utilizador?', default='nao')

    @api.one
    def gen_fatura(self):
        self.user_id.partner_id.gen_fatura()

    @api.model
    def create(self, values):
        values['login'] = values['email']
        values['lang'] = 'pt_PT'
        values['tz'] = 'Europe/Lisbon'
        res = super(Pai, self).create(values)
        pais_group = self.env.ref('gestao_equipas.ges_user_pai')
        pais_group.write({
            'users': [(4, res.user_id.id)]
        })
        return res

    @api.multi
    def write(self, values):
        if 'email' in values:
            values['login'] = values['email']
        return super(Pai, self).write(values)
