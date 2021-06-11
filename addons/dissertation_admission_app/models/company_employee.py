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

    def super_create(self, values):
        return super(CompanyEmployee, self).create(values)

    def check_can_write(self, values):
        is_admin = self.env.user.id == 1 or self.env.user.has_group('dissertation_admission_app.dissertation_admission_group_admin')
        current_courses = set([x.id for x in self.courses])
        try:
            future_courses = set(values['courses'][0][2])
        except:
            future_courses = current_courses
        removed_courses = current_courses - future_courses
        inserted_courses = future_courses - current_courses
        delegated_courses = [x.id for x in self.env.user.delegated_courses]
        can_write_courses = is_admin or all([c in delegated_courses for c in removed_courses.union(inserted_courses)])
        if not can_write_courses:
            raise exceptions.UserError('Não tem permissões para alterar para este conjunto de cursos.')

    @api.model
    def create(self, values):
        self.check_can_write(values)
        user.dissertation_user_create(self.env, values)
        res = self.sudo().super_create(values)
        user.recalculate_permissions(self.env, self.env['res.users'].browse(values['user_id']), 'company_employee')
        return res

    def write(self, vals):
        self.check_can_write(vals)
        return super(CompanyEmployee, self).write(vals)

    def unlink(self):
        user.recalculate_permissions(self.env, self.user_id, None)
        return super(CompanyEmployee, self).unlink()
