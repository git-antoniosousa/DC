from odoo import api, fields, models, exceptions
from . import user



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

    def super_create(self, values):
        return super(Adviser, self).create(values)

    def check_can_write(self, values):
        user.check_can_write_courses(self, values)
        is_admin = self.env.user.id == 1 or self.env.user.has_group('dissertation_admission_app.dissertation_admission_group_admin')
        if 'perms' in values:
            fut_perms = values['perms']
        else:
            fut_perms = self.perms
        can_write_perms = is_admin or self.perms == fut_perms or (self.perms != 'director' and fut_perms != 'director')
        if not can_write_perms:
            raise exceptions.UserError('Não tem permissões para alterar as permissões deste utilizador.')

    @api.model
    def create(self, values):
        self.check_can_write(values)
        user.dissertation_user_create(self.env, values)
        res = self.sudo().super_create(values)
        user.recalculate_permissions(self.env, self.env['res.users'].browse(values['user_id']), res.perms)
        return res

    def write(self, vals):
        self.check_can_write(vals)
        res = super(Adviser, self).write(vals)
        user.recalculate_permissions(self.env, self.user_id, self.perms)
        return res

    def unlink(self):
        user.recalculate_permissions(self.env, self.user_id, None)
        return super(Adviser, self).unlink()
