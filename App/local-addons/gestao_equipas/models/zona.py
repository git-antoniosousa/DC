# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Zona(models.Model):
    _name = 'ges.zona'
    _description = 'Zona'
    _rec_name = 'nome'

    nome = fields.Char(string='Descrição')
