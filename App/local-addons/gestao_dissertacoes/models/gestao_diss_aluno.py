from odoo import api, models, fields


class Student(models.Model):
    _name = "student"
    student_num = fields.Char(string="Número do Aluno", required=True)
    name = fields.Char(string="Nome do Aluno", required=True, translate=True)
    genre = fields.Selection([('m', 'masculino'), ('f', 'feminino')], required=True)

