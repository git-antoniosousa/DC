from odoo import api, fields, models
import base64
import logging


class WorkPlan(models.Model):
    _name = 'dissertation_admission.work_plan'
    _description = 'Plano de Trabalho'

    name = fields.Char(compute='_get_name')
    dissertation = fields.Many2one('dissertation_admission.dissertation', required=True)
    student = fields.Many2one('dissertation_admission.student', required=True)

    # plan = fields.Many2one('ir.attachment')

    def download_latex(self):
        text = open("/mnt/templates/work_plan.tex", "r").read() \
            .replace('$year$', self.dissertation.school_year) \
            .replace('$name$', self.student.name) \
            .replace('$number$', self.student.university_id) \
            .replace('$title$', self.dissertation.name) \
            .replace('$titleen$', self.dissertation.name_en)
        result = base64.b64encode(bytes(text, 'utf-8'))

        base_url = self.sudo().env['ir.config_parameter'].get_param('web.base.url')
        attachment_obj = self.env['ir.attachment']

        attachment_id = attachment_obj.sudo().create(
            {'name': 'plano_trabalho_' + self.student.university_id + '.tex', 'datas': result})

        download_url = '/web/content/' + str(attachment_id.id) + '?download=true'

        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }

    def _get_name(self):
        self.name = self.dissertation.name
