from odoo import models, fields, _, exceptions, api
import time
import random
import logging
import zipfile
import shutil
import os


class SignWizard(models.TransientModel):
    _name = 'dissertation_admission.sign_wizard'
    work_plans = fields.Many2many('dissertation_admission.work_plan'
                                  , relation='dissertation_admission_sign_wizard_rel'
                                  , domain="['&amp;', ('verified', '=', True),"
                                           " '&amp;', ('pdf', '=', True), ('pdf_signed', '=', False)]")
    phone = fields.Char()
    pin = fields.Char()
    otp = fields.Char()

    warning = fields.Integer(default=0)

    def work_plan_calc_fname(self, work_plan):
        return str(work_plan.id) + ".pdf"
        pass

    def confirm_1(self):
        working_dir = '/tmp/sign_wizard_' + str(random.getrandbits(128))
        logging.info("Number of workplans " + str(len(self.work_plans)))
        if not self.phone or not self.pin:
            raise exceptions.UserError("Falta de número telefonico ou pin.")
        if len(self.work_plans) > 50:
            raise exceptions.UserError("Só pode selecionar um máximo de 50 planos para assinar de cada vez.")

        os.makedirs(working_dir)
        try:
            for work_plan in self.work_plans:
                with open(working_dir + "/" + str(work_plan.id) + ".pdf", "w+b") as wpf:
                    wpf.write(work_plan.pdf)

            with zipfile.ZipFile(working_dir + '/work_plan.zip', 'w') as ziph:
                for work_plan in self.work_plans:
                    ziph.write(working_dir + "/" + str(work_plan.id) + ".pdf", arcname=str(work_plan.id) + '.pdf')

            with zipfile.ZipFile(working_dir + '/work_plan.zip', 'r') as ziph:
                logging.info(ziph.namelist())

            ###################
            # TODO: send thing to server
            token = "beautifultoken"
            ###################
        finally:
            shutil.rmtree(working_dir)
        time.sleep(1)

        return {
            'name': _('Assinar Planos de Tese (Passo 2 em 2)'),
            'view_mode': 'form',
            'view_id': self.env.ref('dissertation_admission_app.sign_wizard_form_2').id,
            'view_type': 'form',
            'res_model': 'dissertation_admission.sign_wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': dict(self._context, token=token)
        }

    def confirm_2(self):
        logging.info("Amazing token : " + self._context.get('token'))

        #################
        # TODO: send otp to server
        # TODO: recieve signed docs
        #################

        time.sleep(1)
