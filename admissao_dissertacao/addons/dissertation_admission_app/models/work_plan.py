import io

from odoo import api, fields, exceptions, models, _
import base64
import zipfile


class WorkPlan(models.Model):
    _name = 'dissertation_admission.work_plan'
    _description = 'Plano de Trabalho'

    dissertation = fields.Many2one('dissertation_admission.dissertation', readonly=True, required=True)
    student = fields.Many2one('dissertation_admission.student', readonly=True, required=True)

    pdf = fields.Binary(readonly=True, default=None)
    pdf_fname = fields.Char(compute="_get_pdf_fname")
    pdf_signed = fields.Binary(default=None)
    pdf_signed_fname = fields.Char(compute="_get_pdf_signed_fname")
    verified = fields.Boolean(default=False)
    signed_director = fields.Boolean(compute="_get_signed_director")
    pdf_pre_thesis = fields.Binary(default=None)
    pdf_pre_thesis_fname = fields.Char(compute="_get_pdf_pre_thesis_fname")

    def create(self, vals):
        ndiss = len(self.env['dissertation_admission.work_plan'].sudo() \
                    .search([('dissertation.id', '=', vals['dissertation'])]))
        nstud = len(self.env['dissertation_admission.work_plan'].sudo() \
                    .search([('student.id', '=', vals['student'])]))
        if (ndiss + nstud) != 0:
            raise exceptions.UserError("Já existe um plano de trabalho para esta dissertação/aluno.")
        super(WorkPlan, self).create(vals)

    def download_latex(self):
        with open(f"{self.sudo().env['ir.config_parameter'].get_param('dissertation_templates_dir','/mnt/templates')}/work_plan.tex", "r") as ftext:
            text = ftext.read() \
                .replace('$year$', self.dissertation.school_year.ano_letivo) \
                .replace('$name$', self.student.name) \
                .replace('$number$', self.student.university_id) \
                .replace('$title$', self.dissertation.name) \
                .replace('$titleen$', self.dissertation.name_en)

        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, 'w') as zip_h:
            zip_h.write(f"{self.sudo().env['ir.config_parameter'].get_param('dissertation_templates_dir','/mnt/templates')}/logo.png", arcname='logo.png')
            zip_h.writestr('work_plan.tex', text)

        zip_buf.seek(0)

        return self.create_attachment(base64.b64encode(zip_buf.read()),
                                      'work_plan_' + self.student.university_id + '.zip')

    def download_word(self):
        return self.create_attachment(base64.b64encode(open(f"{self.sudo().env['ir.config_parameter'].get_param('dissertation_templates_dir','/mnt/templates')}/work_plan.docx", "rb").read()),
                                      'work_plan_' + self.student.university_id + '.docx')

    def create_attachment(self, result, name):
        base_url = self.sudo().env['ir.config_parameter'].get_param('web.base.url')
        attachment_obj = self.env['ir.attachment']

        attachment_id = attachment_obj.sudo().create(
            {'name': name, 'datas': result})

        download_url = '/web/content/' + str(attachment_id.id) + '?download=true'

        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }

    def _get_pdf_fname(self):
        self.pdf_fname = 'plano_de_trabalho.pdf'

    def _get_pdf_signed_fname(self):
        self.pdf_signed_fname = 'plano_de_trabalho_assinado.pdf'

    def _get_pdf_pre_thesis_fname(self):
        self.pdf_pre_thesis_fname = 'pre_tese.pdf'

    def _get_signed_director(self):
        self.signed_director = not not self.pdf_signed

    def open_sign_wizard(self):
        return {
            'name': _('Assinar Planos de Tese (Passo 1 em 2)'),
            'view_mode': 'form',
            'view_id': self.env.ref('dissertation_admission_app.sign_wizard_form_1').id,
            'view_type': 'form',
            'res_model': 'dissertation_admission.sign_wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
