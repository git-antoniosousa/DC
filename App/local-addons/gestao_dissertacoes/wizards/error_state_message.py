from odoo import fields, models


class StateErrorMessage(models.TransientModel):
    _name = 'gest.state_error.wizard'
    _description = 'Cancel Message'

    message = fields.Text(string="Existem estados por preencher", readonly=True, store=False)
