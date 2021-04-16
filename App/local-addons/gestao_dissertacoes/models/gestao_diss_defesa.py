from odoo import api, models, fields


class Defesa(models.Model):
    _name = "gest_diss.defesa"
    _description = 'Defesa de um aluno'
    _rec_name = 'data_hora'

    data_hora = fields.Datetime('Data e Hora', required=True)
    local = fields.Selection([('presencial', 'Presencial'), ('virtual', 'Virtual')], required=True)
    sala = fields.Char(string="Sala", required=True)



