# -*- coding: utf-8 -*-


from odoo import models, fields, api


class TempoParte(models.Model):
    _name = 'ges.tempo_parte'
    _description = 'Tempo de cada parte do jogo em minutos'
    _order = 'tempo_parte'
    _rec_name = 'tempo_parte'


    _sql_constraints = [(
        'unique_tempo_parte', 'unique(tempo_parte)', 'Não pode haver duas durações de partes iguais!')
    ]

    tempo_parte = fields.Integer(string="Tempo de cada parte (mins)")
