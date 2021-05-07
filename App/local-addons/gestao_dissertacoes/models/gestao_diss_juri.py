from odoo import api, models, fields


class Juri(models.Model):
    _name = "gest_diss.juri"
    _description = 'Júri'

    juri_presidente_id = fields.Many2one('res.partner', 'Presidente')
    juri_vogal_id = fields.Many2one('res.partner', 'Vogal')
    juri_arguente_id = fields.Many2one('gest_diss.arguente', 'Arguente')
