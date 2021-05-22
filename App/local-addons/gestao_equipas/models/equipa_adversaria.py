# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AtletaAdversario(models.Model):
    _name = 'ges.atleta_adversario'
    _description = 'Atleta adverśario'

    _rec_name = 'nome'

    nome = fields.Char(string='Nome')
    equipa = fields.Many2one(comodel_name='ges.equipa_adversaria',
                             string='Equipa')


class EquipaAdversaria(models.Model):
    _name = 'ges.equipa_adversaria'
    _description = 'Equipa Adversária'
    _rec_name = 'nome'

    nome = fields.Char(string='Nome Equipa')

    atletas = fields.One2many(comodel_name='ges.atleta_adversario',
                              inverse_name='equipa', string='Atletas')


