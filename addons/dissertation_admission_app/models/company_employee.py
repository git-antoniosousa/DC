from odoo import api, fields, models, exceptions
from . import user

class CompanyEmployee(models.Model):
    _name = 'dissertation_admission.company_employee'
    _inherits = {'res.users': 'user_id'}
    _description = 'Orientador'
    user_id = fields.Many2one('res.users', ondelete='restrict', required=True)
    company_id = fields.Many2one('dissertation_admission.company', required=True)
    courses = fields.Many2many('dissertation_admission.course', required=True,
                               relation="dissertation_admission_employee_course_rel")
    @api.model
    def create(self, values):
        assoc_user = self.env['res.users'].browse(values['user_id'])
        values['login'] = assoc_user.login
        values['tz'] = 'Europe/Lisbon'
        user.check_already_assigned(assoc_user)

        res = super(CompanyEmployee, self).create(values)

        assoc_user.recalculate_permissions(self.env, assoc_user, 'company_employee')

        return res

    def write(self, vals):
        vals['user_id'] = self.user_id  # Can't alter associated user
        return super(CompanyEmployee, self).write(vals)

    def unlink(self):
        user.recalculate_permissions(self.env, self.user_id, None)
        return super(CompanyEmployee, self).unlink()
