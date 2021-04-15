from odoo import api, models, fields


class Aluno(models.Model):
    _name = "gest_diss.aluno"
    _description = 'Aluno'

    nome = fields.Char(string="Nome", required=True)
    numero = fields.Char(string="Número", required=True)
    curso = fields.Selection([('miei', 'MIEI'), ('miebiom', 'MIEBIOM')], required=True)
    genero = fields.Selection([('m', 'Masculino'), ('f', 'Feminino')], required=True)
    email = fields.Char(string="Email")

