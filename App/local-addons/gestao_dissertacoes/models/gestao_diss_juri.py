from odoo import api, models, fields


class Juri(models.Model):
    _name = "gest_diss.juri"
    _description = 'Júri'

    juri_presidente_id = fields.Many2one('gest_diss.membro', 'Presidente')
    juri_vogal_id = fields.Many2one('gest_diss.membro', 'Vogal')
    juri_arguente_id = fields.Many2one('gest_diss.membro', 'Arguente')

   # def name_get(self):
   #     data = []
   #     for obj in self:
   #         f = f"(P) {obj.juri_presidente_id.nome} | (V) {obj.juri_vogal_id.nome} | (A) {obj.arguente_id.nome}"
   #         data.append((obj.id, f))
   #     return data
