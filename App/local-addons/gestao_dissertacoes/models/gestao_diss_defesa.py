from odoo import api, models, fields


class Defesa(models.Model):
    _name = "gest_diss.defesa"
    _description = 'Defesa de um aluno'
    _rec_name = 'data_hora'

    data_hora = fields.Datetime('Data e Hora')
    data_defesa = fields.Char(string="Data da Defesa")
    hora_defesa = fields.Char(string="Hora da Defesa")
    local = fields.Selection([('presencial', 'Presencial'), ('virtual', 'Virtual')])
    sala = fields.Char(string="Sala")



