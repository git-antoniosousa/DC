from odoo import models, fields, _, exceptions, api
import time
import logging


class SignWizard(models.TransientModel):
    _name = 'dissertation_admission.sign_wizard'
    work_plans = fields.Many2many('dissertation_admission.work_plan'
                                  , relation='dissertation_admission_sign_wizard_rel')
    phone = fields.Char()
    pin = fields.Char()
    otp = fields.Char()

    warning = fields.Integer(default=0)

    def confirm_1(self):

        time.sleep(2)

        return {
            'name': _('Assinar Planos de Tese (Passo 2 em 2)'),
            'view_mode': 'form',
            'view_id': self.env.ref('dissertation_admission_app.sign_wizard_form_2').id,
            'view_type': 'form',
            'res_model': 'dissertation_admission.sign_wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def confirm_2(self):
        time.sleep(2)
