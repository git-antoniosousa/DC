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
    school_year = fields.Selection([(str(num) + '/' + str(num + 1), str(num) + '/' + str(num + 1))
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

    work_plan_id = fields.Many2one('dissertation_admission.work_plan', string='Plano de Trabalho',
                                   compute="_get_work_plan")

    @api.model
    def create(self, vals):
        ret = super(Dissertation, self).create(vals)
        self.check_valid_courses(vals)
        return ret

    def write(self, vals):
        ret = super(Dissertation, self).write(vals)
        self.check_unique_coadvisers()
        self.check_valid_courses(vals)
        logging.info(vals)
        if not self.work_plan_id and 'student_id' in vals and vals['student_id']:
            return ret and self.env['dissertation_admission.work_plan'].sudo().create({
                'dissertation': self.id,
                'student': vals['student_id']})
        return ret

    def unlink(self):
        for review in self.reviews:
            review.unlink()
        super(Dissertation, self).unlink()

    def register_candidate(self):
        student_uid = self._context.get('uid')
        student = self.env['dissertation_admission.student'].sudo().search([('user_id', '=', student_uid)])[0]
        self.sudo().write({'candidates': [(4, student.id)]})

    def ask_revision(self):
        self.sudo().write({'state': 'pending'})

    def approve(self):
        self.state = 'approved'

    def disapprove(self):
        self.state = 'disapproved'

    def publish(self):
        if self.state == 'approved':
            self.is_public = True

    def unpublish(self):
        self.is_public = False

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

    def _get_work_plan(self):
        try:
            self.work_plan_id = self.env['dissertation_admission.work_plan'].sudo() \
                .search([('dissertation', '=', self.id)])[0]
        except:
            self.work_plan_id = False

    def show_publish_wizard(self):
        return {'type': 'ir.actions.act_window',
                'name': ('Publish Dissertation Wizard View'),
                'res_model': 'dissertation_admission.publish_dissertation_wizard',
                'target': 'new',
                'view_id': self.env.ref('dissertation_admission.publish_dissertation_wizard_view').id,
                'view_mode': 'form',
                'context': {}
                }