from odoo import api, fields, models, exceptions
import logging


_logger = logging.getLogger(__name__)

def check_already_assigned(user):
    if user.student_uid or user.adviser_uid or user.direction_uid:
        raise exceptions.UserError('O utilizador já tem permissões atribuídas para admissões de dissertação.')


def recalculate_permissions(env, user, perms):
    groups = [env.ref('dissertation_admission_app.dissertation_admission_group_user'),
              env.ref('dissertation_admission_app.dissertation_admission_group_student'),
              env.ref('dissertation_admission_app.dissertation_admission_group_coadviser'),
              env.ref('dissertation_admission_app.dissertation_admission_group_adviser'),
              env.ref('dissertation_admission_app.dissertation_admission_group_direction'),
              env.ref('dissertation_admission_app.dissertation_admission_group_course_director')]
    for group in groups:
        group.write({'users': [(3, user.id)]})

    if perms == 'student':
        groups[1].write({'users': [(4, user.id)]})
    elif perms == 'coadviser':
        groups[2].write({'users': [(4, user.id)]})
    elif perms == 'adviser':
        groups[3].write({'users': [(4, user.id)]})
    elif perms == 'direction':
        groups[4].write({'users': [(4, user.id)]})
    elif perms == 'director':
        groups[5].write({'users': [(4, user.id)]})


class StudentUser(models.Model):
    _inherit = 'res.users'
    student_uid = fields.Many2one('dissertation_admission.student', compute='_get_student_id')

    def _get_student_id(self):
        try:
            self.student_uid = self.env['dissertation_admission.student'].sudo().search([('user_id', '=', self.id)])[
                0].id
        except:
            self.student_uid = None


class AdviserUser(models.Model):
    _inherit = 'res.users'
    adviser_uid = fields.Many2one('dissertation_admission.adviser', compute='_get_adviser_id')

    def _get_adviser_id(self):
        try:
            self.adviser_uid = self.env['dissertation_admission.adviser'].sudo().search([('user_id', '=', self.id)])[
                0].id
        except:
            self.adviser_uid = None


class DirectionUser(models.Model):
    _inherit = 'res.users'
    direction_uid = fields.Many2one('dissertation_admission.direction', compute='_get_direction_id')

    def _get_direction_id(self):
        try:
            self.direction_uid = \
                self.env['dissertation_admission.direction'].sudo().search([('user_id', '=', self.id)])[0].id
        except:
            self.direction_uid = None
