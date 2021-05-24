# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LicencaDesportiva(models.Model):
    _name = 'ges.licenca_desportiva'
    _description = 'Licenca Desportiva'
    _order = 'validade DESC'
    _rec_name = 'numero'

    numero = fields.Char('Número Licença', required=True)
    validade = fields.Date('Validade Licença')
    atleta_id = fields.Many2one('ges.atleta',
                                'Atleta',
                                ondelete='cascade')
    treinador_id = fields.Many2one('ges.treinador',
                                   'Treinador',
                                   ondelete='cascade')
    seccionista_id = fields.Many2one('ges.seccionista',
                                   'Seccionista',
                                   ondelete='cascade')
