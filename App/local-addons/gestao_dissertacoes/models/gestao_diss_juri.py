from odoo import api, models, fields


class Juri(models.Model):
    _name = "gest_diss.juri"
    _description = 'Júri'

    juri_presidente_id = fields.Many2one('res.partner', 'Presidente')
    juri_vogal_id = fields.Many2one('res.partner', 'Vogal')
    juri_arguente_id = fields.Many2one('res.partner', 'Arguente')

    def name_get(self):
        data = []
        for obj in self:
            f = f"(P) {obj.juri_presidente_id.name} | (V) {obj.juri_vogal_id.name} | (A) {obj.juri_arguente_id.name}"
            data.append((obj.id, f))
        return data
