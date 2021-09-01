from odoo import api, fields, models, exceptions
from . import user

class Student(models.Model):
    _name = 'dissertation_admission.student'
    _inherits = {'res.users': 'user_id'}
    _description = 'Estudante'
    user_id = fields.Many2one('res.users', required=True, ondelete='restrict')
    university_id = fields.Char(required=True)
    course = fields.Many2one('gest_diss.curso', required=True)

    def super_create(self, values):
        return super(Student, self).create(values)

    def check_can_write(self, values):
        can_write = self.env.user.id == 1 or \
                    self.env.user.has_group('dissertation_admission_app.dissertation_admission_group_admin') or \
                    values['course'] in [x.id for x in self.env.user.delegated_courses]
        if not can_write:
            raise exceptions.UserError('Não tem permissões para adicionar um aluno a este curso.')

    @api.model
    def create(self, values):
        self.check_can_write(values)
        user.dissertation_user_create(self.env, values)
        res = self.sudo().super_create(values)
        user.recalculate_permissions(self.env, self.env['res.users'].browse(values['user_id']), 'student')
        return res

    def write(self, vals):
        self.check_can_write(vals)
        return super(Student, self).write(vals)

    def unlink(self):
        user.recalculate_permissions(self.env, self.user_id, None)
        return super(Student, self).unlink()
