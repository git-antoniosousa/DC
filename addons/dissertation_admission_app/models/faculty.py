from odoo import api, fields, models
from odoo.exceptions import Warning


class Faculty(models.Model):
    _inherit = 'res.users'

    faculty_number = fields.Integer('número mecanográfico')
    faculty_course = fields.Text('Curso')
    faculty_investigation_center = fields.Text('Centro de investigações')
