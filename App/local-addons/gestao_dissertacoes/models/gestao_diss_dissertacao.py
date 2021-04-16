from odoo import api, models, fields


class Dissertacao(models.Model):
    _name = "gest_diss.dissertacao"
    _description = 'Dissertação de um aluno'
    _rec_name = "titulo"

    titulo = fields.Char(string="Título", required=True)
    orientador = fields.Many2one('gest_diss.docente', required=True)
    nota = fields.Integer(string="Nota", required=True)
