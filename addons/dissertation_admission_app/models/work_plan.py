from odoo import api, fields, models, _
import base64
import logging
import random
import os
import zipfile
import shutil


class WorkPlan(models.Model):
    _name = 'dissertation_admission.work_plan'
    _description = 'Plano de Trabalho'

    name = fields.Char(compute='_get_name')
    dissertation = fields.Many2one('dissertation_admission.dissertation', required=True)
    student = fields.Many2one('dissertation_admission.student', required=True)

    def download_latex(self):
        working_dir = '/tmp/work_plan_' + str(random.getrandbits(128))
        os.makedirs(working_dir)

        with open("/mnt/templates/work_plan.tex", "r") as ftext:
            text = ftext.read() \
                .replace('$year$', self.dissertation.school_year) \
                .replace('$name$', self.student.name) \
                .replace('$number$', self.student.university_id) \
                .replace('$title$', self.dissertation.name) \
                .replace('$titleen$', self.dissertation.name_en)

        with open(working_dir + '/work_plan.tex', 'w') as wp_file:
            wp_file.write(text)

        with zipfile.ZipFile(working_dir + '/work_plan.zip', 'w') as ziph:
            ziph.write('/mnt/templates/logo.png', arcname='logo.png')
            ziph.write(working_dir + '/work_plan.tex', arcname='work_plan.tex')

        with open(working_dir + '/work_plan.zip', 'rb') as zipf:
            result = base64.b64encode(zipf.read())

        shutil.rmtree(working_dir)

        base_url = self.sudo().env['ir.config_parameter'].get_param('web.base.url')
        attachment_obj = self.env['ir.attachment']

        attachment_id = attachment_obj.sudo().create(
            {'name': 'work_plan_' + self.student.university_id + '.zip', 'datas': result})

        download_url = '/web/content/' + str(attachment_id.id) + '?download=true'

        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }

    def _get_name(self):
        self.name = self.dissertation.name

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