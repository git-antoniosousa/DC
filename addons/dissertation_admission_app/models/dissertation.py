from odoo import api, fields, models
from odoo import exceptions
import logging
import datetime

class Dissertation(models.Model):
    states = [
        ('disapproved', 'Reprovado'),
        ('pending', 'Aprovação Pendente'),
        ('approved', 'Aprovado')
    ]
    _name = 'dissertation_admission.dissertation'
    _description = 'Dissertação'

    name = fields.Char('Titulo', required=True)
    description = fields.Text(string='Descrição', required=True)
    state = fields.Selection(states, string='Estado', required=True, default='pending')
    school_year = fields.Selection([(str(num), str(num) + '/' + str(num + 1))
                                    for num in range(2020, datetime.datetime.now().year)]
                                   , required=True)
    is_public = fields.Boolean(string='Publico?', required=True, default=False)
    course = fields.Many2many('dissertation_admission.course',
                              relation='dissertation_admission_dissertation_course_rel')
    adviser_id = fields.Many2one('res.users', string='Orientador')
    coadviser_id = fields.Many2one('res.users', string='Coorientador')
    student_id = fields.Many2one('dissertation_admission.student', string='Estudante')
    candidates = fields.Many2many('dissertation_admission.student', readonly=True
                                  , relation='dissertation_admission_dissertation_candidates_rel')
    reviews = fields.Many2many('dissertation_admission.dissertation_review'
                               , relation='dissertation_admission_dissertation_review_rel')

    def write(self, vals):
        super(Dissertation, self).write(vals)

    def register_candidate(self):
        student_uid = self._context.get('uid')
        student = self.env['dissertation_admission.student'].sudo().search([('user_id', '=', student_uid)])[0]
        self.sudo().write({'candidates': [(4, student.id)]})

    def _get_reviews(self):
        self.reviews = self.env['dissertation_admission.dissertation_review'].sudo() \
            .search([('dissertation', '=', self.id)])
