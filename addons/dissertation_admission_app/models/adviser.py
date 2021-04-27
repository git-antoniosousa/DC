from odoo import api, fields, models, exceptions
import logging

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
        values['login'] = self.env['res.users'].browse(values['user_id']).email
        values['tz'] = 'Europe/Lisbon'
        res = super(Adviser, self).create(values)

        if not res.coadviser_only:
            group = self.env.ref('dissertation_admission_app.dissertation_admission_group_adviser')
            group.write({'users': [(4, res.user_id.id)]})

        return res
