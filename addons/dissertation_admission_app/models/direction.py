from odoo import api, fields, models, exceptions
import logging
from . import user

_logger = logging.getLogger(__name__)


class Direction(models.Model):
    _name = 'dissertation_admission.direction'
    _inherits = {'res.users': 'user_id'}
    _description = 'Secretaria de Curso'
    user_id = fields.Many2one('res.users', ondelete='restrict', required=True)
    university_id = fields.Char()
    courses = fields.Many2many('dissertation_admission.course', required=True,
                               relation="dissertation_admission_direction_course_rel")

    def super_create(self, values):
        return super(Direction, self).create(values)

    @api.model
    def create(self, values):
        user.dissertation_user_create(self.env, values)
        res = self.sudo().super_create(values)
        user.recalculate_permissions(self.env, self.env['res.users'].browse(values['user_id']), 'direction')
        return res

    def unlink(self):
        user.recalculate_permissions(self.env, self.user_id, None)
        return super(Direction, self).unlink()
