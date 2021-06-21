from odoo import fields, models


class JuriNaoPreenchido(models.TransientModel):
    _name = 'gest.juri_nao_preenchido.wizard'
    _description = 'Error Message'

    message = fields.Text(string="Faltam dados do Júri para preencher", readonly=True, store=False)
