from odoo import api, models, fields


class Defesa(models.Model):
    _name = "gest_diss.defesa"
    _description = 'Defesa de um aluno'

    data_hora = fields.Datetime('Data e Hora', required=True)
    local = fields.Selection([('presencial', 'Presencial'), ('virtual', 'Virtual')], required=True)
    sala = fields.Char(string="Sala", required=True)
#    arguente = fields.One2one('gest_diss.arguente', required=True)
 #   presidente = fields.One2one('gest_diss.docente', required=True)
  #  vogal_1 = fields.One2many('gest_diss.docente', required=True)
   # vogal_2 = fields.One2many('gest_diss.docente', required=True)


