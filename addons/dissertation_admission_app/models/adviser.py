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
    department = fields.Many2one('dissertation_admission.department', required=True)
    courses = fields.Many2many('dissertation_admission.course', required=True,
                               relation="dissertation_admission_adviser_course_rel")
    investigation_center = fields.Many2many('dissertation_admission.investigation_center', required=True,
                                            relation="dissertation_admission_adviser_investigation_center_rel")
    perms = fields.Selection(perms, required=True, default='pending')

    @api.model
    def create(self, values):
        if 'password' in values and values['password'] is False:
            del values['password']
        assoc_user = self.env['res.users'].browse(values['user_id'])
        values['login'] = assoc_user.login
        values['tz'] = 'Europe/Lisbon'
        user.check_already_assigned(assoc_user)
        res = super(Adviser, self).create(values)
        user.recalculate_permissions(self.env, assoc_user, res.perms)
        return res

    def write(self, vals):
        res = super(Adviser, self).write(vals)
        _logger.info('\n\n\n\n\n')
        _logger.info(str(self.perms))
        user.recalculate_permissions(self.env, self.user_id, self.perms)
        return res

    def unlink(self):
        user.recalculate_permissions(self.env, self.user_id, None)
        return super(Adviser, self).unlink()
