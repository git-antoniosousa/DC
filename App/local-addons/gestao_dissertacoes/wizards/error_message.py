from odoo import fields, models


class ErrorMessage(models.TransientModel):
    _name = 'gest.wizard'
    _description = 'Cancel Message'

    message = fields.Text(string="Faltam preencher alguns campos", readonly=True, store=False)
