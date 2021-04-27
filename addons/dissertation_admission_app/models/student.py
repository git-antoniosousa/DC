from odoo import api, fields, models, exceptions
import logging

_logger = logging.getLogger(__name__)

class Student(models.Model):
    _name = 'dissertation_admission.student'
    _inherits = {'res.users': 'user_id'}
    _description = 'Estudante'
    user_id = fields.Many2one('res.users', ondelete='restrict', required=True)
    university_id = fields.Char(required=True)
    course = fields.Many2one('dissertation_admission.course', required=True)

    @api.model
    def create(self, values):
        values['login'] = self.env['res.users'].browse(values['user_id']).email
        values['tz'] = 'Europe/Lisbon'
        res = super(Student, self).create(values)

        student_group = self.env.ref('dissertation_admission_app.dissertation_admission_group_student')
        student_group.write({'users': [(4, res.user_id.id)]})

        return res