from odoo import api, fields, models, exceptions
import logging

_logger = logging.getLogger(__name__)


def dissertation_user_create(env, values):
    if 'password' in values and values['password'] is False:
        del values['password']
    assoc_user = env['res.users'].browse(values['user_id'])
    values['login'] = assoc_user.login
    values['tz'] = 'Europe/Lisbon'
    check_already_assigned(assoc_user)


def check_already_assigned(user):
    if user.student_uid or user.adviser_uid or user.direction_uid or user.company_employee_uid:
        raise exceptions.UserError('O utilizador já tem permissões atribuídas para admissões de dissertação.')


def recalculate_permissions(env, user, perms):
    groups = [env.ref('dissertation_admission_app.dissertation_admission_group_user'),
              env.ref('dissertation_admission_app.dissertation_admission_group_student'),
              env.ref('dissertation_admission_app.dissertation_admission_group_coadviser'),
              env.ref('dissertation_admission_app.dissertation_admission_group_adviser'),
              env.ref('dissertation_admission_app.dissertation_admission_group_direction'),
              env.ref('dissertation_admission_app.dissertation_admission_group_course_director'),
              env.ref('dissertation_admission_app.dissertation_admission_group_company_employee')]
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
    elif perms == 'company_employee':
        groups[6].write({'users': [(4, user.id)]})


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


class CompanyEmployeeUser(models.Model):
    _inherit = 'res.users'
    company_employee_uid = fields.Many2one('dissertation_admission.company_employee', compute='_get_employee_id')

    def _get_employee_id(self):
        try:
            self.company_employee_uid = \
                self.env['dissertation_admission.company_employee'].sudo().search([('user_id', '=', self.id)])[0].id
        except:
            self.company_employee_uid = None


class UserCourses(models.Model):
    _inherit = 'res.users'
    delegated_courses = fields.Many2many('dissertation_admission.course', compute='_get_courses',
                                         relation='dissertation_admission_dissertation_user_course_rel')

    def _get_courses(self):
        try:
            self.delegated_courses = \
                (self.company_employee_uid or self.direction_uid or self.adviser_uid).courses
            logging.info(self.delegated_courses)
        except:
            self.delegated_courses = None
