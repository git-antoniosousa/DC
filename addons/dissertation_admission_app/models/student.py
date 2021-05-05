from odoo import api, fields, models, exceptions
import logging
from . import dissertation_user

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
        user = self.env['res.users'].browse(values['user_id'])
        values['login'] = user.email
        values['tz'] = 'Europe/Lisbon'
        dissertation_user.check_already_assigned(user)

        res = super(Student, self).create(values)

        dissertation_user.recalculate_permissions(self.env, user, 'student')

        return res

    def write(self, vals):
        vals['user_id'] = self.user_id  # Can't alter associated user
        return super(Student, self).write(vals)

    def unlink(self):
        dissertation_user.recalculate_permissions(self.env, self.user_id, None)
        return super(Student, self).unlink()
