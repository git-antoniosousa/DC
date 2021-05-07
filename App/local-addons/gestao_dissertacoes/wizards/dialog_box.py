from odoo import fields, models


class DialogBox(models.TransientModel):
    _name = 'gest.wiz.dialog.box'

    title = fields.Char(string='Title', readonly=True)
    text = fields.Char(string='Text', readonly=True)