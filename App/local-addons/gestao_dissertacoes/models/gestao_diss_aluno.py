from odoo import api, models, fields


class Aluno(models.Model):
    _name = "gest_diss.aluno"
    numero = fields.Char(string="Número", required=True)
    nome = fields.Char(string="Nome", required=True)
    curso = fields.Selection([('MIEI', 'MIEI'), ('MIEBIOM', 'MIEBIOM')], required=True)
    genero = fields.Selection([('m', 'masculino'), ('f', 'feminino')], required=True)
    email = fields.Char(string="Email")

