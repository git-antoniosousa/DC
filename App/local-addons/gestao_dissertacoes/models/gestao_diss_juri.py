from odoo import api, models, fields


class Juri(models.Model):
    _name = "gest_diss.juri"
    _description = 'Júri'
    _rec_name = "juri_presidente_id"

    juri_presidente_id = fields.Many2one('gest_diss.docente', 'Presidente')
    juri_vogal_id = fields.Many2one('gest_diss.docente', 'Vogal')
    arguente_id = fields.Many2one('gest_diss.arguente', 'Arguente')

    def name_get(self):
        data = []
        for obj in self:
            f = f"(P) {obj.juri_presidente_id.nome} | (V) {obj.juri_vogal_id.nome} | (A) {obj.arguente_id.nome}"
            data.append((obj.id, f))
        return data