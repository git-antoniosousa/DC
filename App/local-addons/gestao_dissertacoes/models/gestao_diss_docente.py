from odoo import api, models, fields


class Docente(models.Model):
    _name = "gest_diss.docente"
    _description = 'Docente'

    nome = fields.Char(string="Nome", required=True)
    numero = fields.Char(string="Nome", required=True)
    cargo = fields.One2one('gest_diss.aluno', required=True)
    email = fields.One2one('gest_diss.docente')