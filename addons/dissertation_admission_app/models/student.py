from odoo import api, fields, models, exceptions
import logging
from . import user

class Student(models.Model):
    _name = 'dissertation_admission.student'
    _inherits = {'res.users': 'user_id'}
    _description = 'Estudante'
    user_id = fields.Many2one('res.users', ondelete='restrict', required=True)
    university_id = fields.Char(required=True)
    course = fields.Many2one('dissertation_admission.course', required=True)

    @api.model
    def create(self, values):
        assoc_user = self.env['res.users'].browse(values['user_id'])
        values['login'] = assoc_user.login
        values['tz'] = 'Europe/Lisbon'
        user.check_already_assigned(assoc_user)

        res = super(Student, self).create(values)

        user.recalculate_permissions(self.env, assoc_user, 'student')

        return res

    def write(self, vals):
        vals['user_id'] = self.user_id  # Can't alter associated user
        return super(Student, self).write(vals)

    def unlink(self):
        user.recalculate_permissions(self.env, self.user_id, None)
        return super(Student, self).unlink()
