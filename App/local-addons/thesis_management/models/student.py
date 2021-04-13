from odoo import api, models, fields


class Student(models.Model):
    _name = "student"
    student_num = fields.Char(string="Student Number", required=True)
    name = fields.Char(string="Student Name", required=True, translate=True)
    genre = fields.Selection([('m', 'male'), ('f', 'female')], required=True)

