from odoo import api, models, fields


class Juri(models.Model):
    _name = "gest_diss.juri"
    _description = 'Júri'

    juri_presidente_id = fields.Many2one('gest_diss.membro', 'Presidente')

    convite_presidente = fields.Selection([('aguardar', 'A aguardar resposta.'), ('aceitado', 'Convite aceite.'), ('rejeitado', 'Convite rejeitado.')], string="Convite Presidente", default='aguardar')

    convite_presidente_url = fields.Char(string="Link Convite Presidente")

    juri_vogal_id = fields.Many2one('gest_diss.membro', 'Vogal')

    convite_vogal = fields.Selection([('aguardar', 'A aguardar resposta.'), ('aceitado', 'Convite aceite.'), ('rejeitado', 'Convite rejeitado.')], string="Convite Vogal", default='aguardar')

    convite_vogal_url = fields.Char(string="Link Convite Vogal")

    juri_arguente_id = fields.Many2one('gest_diss.membro', 'Arguente')

    convite_arguente = fields.Selection([('aguardar', 'A aguardar resposta.'), ('aceitado', 'Convite aceite.'), ('rejeitado', 'Convite rejeitado.')], string="Convite Arguente", default='aguardar')

    convite_arguente_url = fields.Char(string="Link Convite Arguente")

    convites_aceites = fields.Integer(string="Convites aceites")

   # def name_get(self):
   #     data = []
   #     for obj in self:
   #         f = f"(P) {obj.juri_presidente_id.nome} | (V) {obj.juri_vogal_id.nome} | (A) {obj.arguente_id.nome}"
   #         data.append((obj.id, f))
   #     return data
