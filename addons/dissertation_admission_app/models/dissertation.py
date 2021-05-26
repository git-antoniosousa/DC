from odoo import api, fields, models
from odoo import exceptions
import datetime
import logging


class Dissertation(models.Model):
    states = [
        ('disapproved', 'Reprovado'),
        ('pending', 'Aprovação Pendente'),
        ('approved', 'Aprovado')
    ]
    _name = 'dissertation_admission.dissertation'
    _description = 'Dissertação'

    name = fields.Char('Titulo Português', required=True)
    name_en = fields.Char('Titulo Inglês', required=True)
    description = fields.Text(string='Descrição', required=True)
    state = fields.Selection(states, string='Estado', required=True, default='pending')
    school_year = fields.Selection([(str(num), str(num) + '/' + str(num + 1))
                                    for num in range(2020, datetime.datetime.now().year)]
                                   , required=True)
    is_public = fields.Boolean(string='Publico?', required=True, default=False)
    course = fields.Many2many('dissertation_admission.course',
                              relation='dissertation_admission_dissertation_course_rel')
    adviser_id = fields.Many2one('dissertation_admission.adviser', string='Orientador')
    coadviser_id_internal = fields.Many2one('dissertation_admission.adviser', string='Coorientador')
    coadviser_id_external = fields.Many2one('dissertation_admission.company_employee', string='Coorientador')
    student_id = fields.Many2one('dissertation_admission.student', string='Estudante')
    candidates = fields.Many2many('dissertation_admission.student', readonly=True
                                  , relation='dissertation_admission_dissertation_candidates_rel')
    reviews = fields.Many2many('dissertation_admission.dissertation_review'
                               , relation='dissertation_admission_dissertation_review_rel')

    @api.model
    def create(self, vals):
        ret = super(Dissertation, self).create(vals)
        self.check_valid_courses(vals)
        return ret

    def write(self, vals):
        ret = super(Dissertation, self).write(vals)
        self.check_unique_coadvisers()
        self.check_valid_courses(vals)
        return ret

    def register_candidate(self):
        student_uid = self._context.get('uid')
        student = self.env['dissertation_admission.student'].sudo().search([('user_id', '=', student_uid)])[0]
        self.sudo().write({'candidates': [(4, student.id)]})

    def ask_revision(self):
        self.sudo().write({'state': 'pending'})

    def check_unique_coadvisers(self):
        if len(self.coadviser_id_external) + len(self.coadviser_id_internal) >= 2:
            raise exceptions.ValidationError("Não pode selecionar dois coorientadores.")

    def check_valid_courses(self, vals):
        try:
            usr = (self.create_uid or self.env.user)
            for course_id in vals['course'][0][2]:
                if course_id not in list(map(lambda x: x.id, usr.delegated_courses)):
                    raise exceptions.ValidationError("")
        except exceptions.ValidationError:
            raise exceptions.ValidationError("Cursos não delegados pelo criador foram selecionados.")
        except Exception:
            pass

    def _get_reviews(self):
        self.reviews = self.env['dissertation_admission.dissertation_review'].sudo() \
            .search([('dissertation', '=', self.id)])
