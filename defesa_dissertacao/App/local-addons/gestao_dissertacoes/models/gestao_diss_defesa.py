from odoo import api, models, fields


class Defesa(models.Model):
    _name = "gest_diss.defesa"
    _description = 'Defesa de um aluno'
    _rec_name = 'data_hora'

    data_hora = fields.Datetime('Data e Hora')

    data_defesa = fields.Char(string="Data da Defesa")
    hora_defesa = fields.Char(string="Hora da Defesa")

    data_words = fields.Char(string="Data em Formato por Extenso")
    hora_words = fields.Char(string="Hora em Formato por Extenso")

    # Exemplo: 12.Jun.2021
    data_str = fields.Char(string="Data em Formato Semi-Extenso")
    # Exemplo: 14h00
    hora_str = fields.Char(string="Hora em Formato por Semi-Extenso")

    local = fields.Selection([('presencial', 'Presencial'), ('virtual', 'Virtual')])
    sala = fields.Char(string="Sala")

