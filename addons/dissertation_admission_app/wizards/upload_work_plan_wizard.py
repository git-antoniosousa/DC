from odoo import models, fields, exceptions
import logging

class UploadWorkPlanWizard(models.TransientModel):
    _name = 'dissertation_admission.upload_work_plan_wizard'

    pdf = fields.Binary(required=True, attachment=True)

    def confirm_work_plan(self):
        uid = self._context.get('uid')
        work_plan = self.env['dissertation_admission.work_plan'].sudo() \
            .search([('student.user_id.id', '=', uid)])
        work_plan.sudo().write({
            "pdf": self.pdf,
            "pdf_signed": None,
            "signed_director": False,
            "verified": False,
        })

    def confirm_pre_thesis(self):
        uid = self._context.get('uid')
        work_plan = self.env['dissertation_admission.work_plan'].sudo() \
            .search([('student.user_id.id', '=', uid)])
        work_plan.sudo().write({
            "pdf_pre_thesis": self.pdf,
        })
