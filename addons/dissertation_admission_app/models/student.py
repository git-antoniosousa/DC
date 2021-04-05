from odoo import api, fields, models
from odoo.exceptions import Warning


class Student(models.Model):
    _inherit = 'res.users'

    student_number = fields.Integer('número mecanográfico')
    student_course = fields.Integer('Curso')
