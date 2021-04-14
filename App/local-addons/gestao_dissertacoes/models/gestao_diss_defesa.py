from odoo import api, models, fields


class Defesa(models.Model):
    _name = "gest_diss.defesa"
    _description = 'Defesa de um aluno'

    data = fields.Char(string="Título", required=True)
    hora = fields.One2one('gest_diss.aluno', required=True)
    local = fields.One2one('gest_diss.docente', required=True) # opção entre presencial ou virtual
    sala = fields.One2one('gest_diss.docente', required=True) # link zoom ou sala fisica
    arguente = fields.One2one('gest_diss.docente', required=True)
    presidente = fields.One2one('gest_diss.docente', required=True)
    vogais = fields.One2many('gest_diss.docente', required=True)
