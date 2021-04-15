from odoo import api, models, fields


class Student(models.Model):
    _name = "student"
    student_num = fields.Char(string="Número Mecanográfico", required=True)
    name = fields.Char(string="Nome", required=True, translate=True)
    genre = fields.Selection([('m', 'Masculino'), ('f', 'Feminino'), ('o', 'Outro')], required=True)

