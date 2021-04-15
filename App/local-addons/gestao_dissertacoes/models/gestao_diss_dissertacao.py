from odoo import api, models, fields


class Dissertacao(models.Model):
    _name = "gest_diss.dissertacao"
    _description = 'Dissertação de um aluno'

    titulo = fields.Char(string="Título", required=True)
    #aluno = fields.One2one('gest_diss.aluno', required=True)
    #docente = fields.One2one('gest_diss.docente', required=True)
    nota = fields.Integer(string="Nota", required=True)

