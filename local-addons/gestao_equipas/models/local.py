# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Local(models.Model):
    _name = 'ges.local'
    _description = 'Local'
    _order = 'descricao'
    _rec_name = 'descricao'

    descricao = fields.Char('Descrição', required=True)
    coordenadas = fields.Char('Coordenadas', required=False)
    googlemaps = fields.Char('Google Maps', required = False)
