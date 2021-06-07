from odoo import api, fields, models, exceptions
import logging
from . import user

_logger = logging.getLogger(__name__)


class Adviser(models.Model):
    perms = [
        ('coadviser', 'Coorientador'),
        ('adviser', 'Orientador'),
        ('director', 'Diretor de Curso')
    ]
    _name = 'dissertation_admission.adviser'
    _inherits = {'res.users': 'user_id'}
    _description = 'Orientador'
    user_id = fields.Many2one('res.users', ondelete='restrict', required=True)
    university_id = fields.Char(required=True)
    department = fields.Char()
    courses = fields.Many2many('dissertation_admission.course', required=True,
                               relation="dissertation_admission_adviser_course_rel")
    investigation_center = fields.Char()
    perms = fields.Selection(perms, required=True, default='pending')

    @api.model
    def create(self, values):
        user.dissertation_user_create(self.env, values)
        res = super(Adviser, self).create(values)
        user.recalculate_permissions(self.env, self.env['res.users'].browse(values['user_id']), res.perms)
        return res

    def write(self, vals):
        res = super(Adviser, self).write(vals)
        user.recalculate_permissions(self.env, self.user_id, self.perms)
        return res

    def unlink(self):
        user.recalculate_permissions(self.env, self.user_id, None)
        return super(Adviser, self).unlink()
