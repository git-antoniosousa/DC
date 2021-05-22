# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta, date


class Treinador(models.Model):
    _name = 'ges.treinador'
    _inherits = {'res.users': 'user_id'}
    _description = 'Treinador'
    _order = 'name'
    _rec_name = 'name'

    user_id = fields.Many2one('res.users',
                              ondelete='restrict',
                              required=True)
    data_admissao = fields.Date('Data de admissão',
                                required=True,
                                default=fields.date.today())
    numero_registo_criminal = fields.Char('Número Registo Criminal', write=['ges_membro_direcao_clube'])
    validade_registo_criminal = fields.Date('Validade Registo Criminal', write=['ges_membro_direcao_clube'])
    licencas_desportivas = fields.One2many('ges.licenca_desportiva',
                                           'treinador_id',
                                           'Licenças Desportivas')
    validade_licenca_desportiva = fields.Date('Validade da licença desportiva',
                                              compute='get_validade_licenca',
                                              store=True)
    treinos = fields.One2many('ges.treino', 'treinador', string='Treinos')
    utilizador_existe = fields.Selection([('sim', 'Sim'),
                                          ('nao', 'Não')],
                                         'Já registado como outro utilizador?', default='nao')

    @api.one
    @api.depends('licencas_desportivas.validade')
    def get_validade_licenca(self):
        if len(self.licencas_desportivas) == 0:
            return
        d = date.min
        for licenca in self.licencas_desportivas:
            dL = fields.Date.from_string(licenca.validade)
            if (dL > d):
                d = dL
        self.validade_licenca_desportiva = d

    @api.one
    def gen_fatura(self):
        self.user_id.partner_id.gen_fatura()

    @api.model
    def create(self, values):
        values['login'] = values['email']
        values['lang'] = 'pt_PT'
        values['tz'] = 'Europe/Lisbon'
        res = super(Treinador, self).create(values)
        treinadores_group = self.env.ref('gestao_equipas.ges_user_treinador')
        treinadores_group.write({
            'users': [(4, res.user_id.id)]
        })
        return res

    @api.multi
    def write(self, values):
        if 'email' in values:
            values['login'] = values['email']
        return super(Treinador, self).write(values)
