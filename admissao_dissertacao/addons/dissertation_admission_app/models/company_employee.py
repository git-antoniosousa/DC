from odoo import api, fields, models, exceptions
from . import user

class CompanyEmployee(models.Model):
    _name = 'dissertation_admission.company_employee'
    _inherits = {'res.users': 'user_id'}
    _description = 'Orientador'
    user_id = fields.Many2one('res.users', ondelete='restrict', required=True)
    company_id = fields.Many2one('dissertation_admission.company', required=True)
    courses = fields.Many2many('gest_diss.curso', required=True)

    def super_create(self, values):
        return super(CompanyEmployee, self).create(values)

    @api.model
    def create(self, values):
        user.check_can_write_courses(self, values)
        user.dissertation_user_create(self.env, values)
        res = self.sudo().super_create(values)
        user.recalculate_permissions(self.env, self.env['res.users'].browse(values['user_id']), 'company_employee')
        return res

    def write(self, vals):
        user.check_can_write_courses(self, vals)
        return super(CompanyEmployee, self).write(vals)

    def unlink(self):
        user.recalculate_permissions(self.env, self.user_id, None)
        return super(CompanyEmployee, self).unlink()
