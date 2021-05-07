from odoo import api, models, fields


class Juri(models.Model):
    _name = "gest_diss.juri"
    _description = 'Júri'
    _rec_name = "juri_presidente_id"

    juri_presidente_id = fields.Many2one('res.partner', 'Presidente')
    juri_vogal_id = fields.Many2one('res.partner', 'Vogal')
    arguente_id = fields.Many2one('res.partner', 'Arguente')

    def name_get(self):
        data = []
        for obj in self:
            f = f"(P) {obj.juri_presidente_id.nome} | (V) {obj.juri_vogal_id.nome} | (A) {obj.arguente_id.nome}"
            data.append((obj.id, f))
        return data