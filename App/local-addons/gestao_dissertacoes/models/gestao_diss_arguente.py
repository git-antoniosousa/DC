from odoo import api, models, fields


class Arguente(models.Model):
    _name = "gest_diss.arguente"
    _description = 'Arguente'

    nome = fields.Char(string="Nome", required=True)
    entidade_patronal = fields.Char(string="Nome", required=True)
    cargo = fields.One2one('gest_diss.aluno', required=True)
    contacto = fields.One2one('gest_diss.docente', required=True) # opção entre presencial ou virtual