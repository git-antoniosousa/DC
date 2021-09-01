import base64
import io
import json
import re
import sys

import requests
from odoo import models, fields, _, exceptions
import logging
import zipfile


class SignWizard(models.TransientModel):
    _name = 'dissertation_admission.sign_wizard'
    _description = 'Sign wizard'
    work_plans = fields.Many2many('dissertation_admission.work_plan'
                                  , relation='dissertation_admission_sign_wizard_rel')
    phone = fields.Char()
    pin = fields.Char()
    otp = fields.Char()

    def work_plan_calc_fname(self, work_plan):
        return str(work_plan.id) + ".pdf"
        pass

    def confirm_1(self):
        if not self.phone or not self.pin:
            raise exceptions.UserError("Falta de número telefonico ou pin.")
        if len(self.work_plans) > 50:
            raise exceptions.UserError("Só pode selecionar um máximo de 50 planos para assinar de cada vez.")

        files = []
        for work_plan in self.work_plans:
            files.append(('file', (str(work_plan.id) + '.pdf', base64.decodebytes(work_plan.pdf), 'application/pdf')))

        cfg = self.get_cfg()

        endpoint = "/requestsign"
        params = {
            'userid': str(self.phone),
            'pin': str(self.pin),
            'x': int(cfg["signature_server"]["x_sig"]),
            'y': int(cfg["signature_server"]["y_sig"]),
        }
        r = self.server_request(endpoint, lambda url: requests.post(url, files=[
            ('params', ('params', bytes(json.dumps(params), 'UTF-8'), 'application/json')),
            *files,
        ]))

        token = r.json()['operationID']

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
        token = self._context.get('token')

        endpoint = "/fetchsign"

        r = self.server_request(endpoint, lambda url: requests.post(url, json={
            'operationID': token,
            'otp': self.otp,
        }))

        with zipfile.ZipFile(io.BytesIO(r.content), "r") as zipf:
            pdf_regex = re.compile("[0-9]+.*\\.pdf")
            id_regex = re.compile("[0-9]+")
            logging.info(zipf.namelist())
            for name in zipf.namelist():
                if pdf_regex.match(name):
                    try:
                        wp_id = int(name[slice(*id_regex.match(name).span())])
                        self.env['dissertation_admission.work_plan'].sudo().search([('id', '=', wp_id)])[0].write({
                            'pdf_signed': base64.b64encode(zipf.read(name))
                        })
                    except Exception as _e:
                        pass

    def get_cfg(self):
        try:
            with open("/mnt/config/config.json", "r") as fconfig:
                cfg = json.loads(fconfig.read())
            assert "host" in cfg["signature_server"]
            assert "port" in cfg["signature_server"]
            assert "x_sig" in cfg["signature_server"]
            assert "y_sig" in cfg["signature_server"]
            return cfg
        except:
            raise exceptions.ValidationError("Erro na configuração da localização do servidor de assinaturas.\n"
                                             "Por favor contacte um administrador.")

    def server_request(self, endpoint, req_fn):
        cfg = self.get_cfg()

        try:
            url = cfg["signature_server"]["host"] + ":" + str(cfg["signature_server"]["port"]) + endpoint
            r = req_fn(url)
        except Exception as e:
            raise exceptions.ValidationError("Erro na comunicação com o servidor de assinaturas.\n"
                                             "Contacte um administrador.\n" + str(e))

        if not 200 <= r.status_code < 300:
            raise exceptions.ValidationError("Servidor de assinaturas reportou um erro.\n"
                                             "Por favor verifique os dados introduzidos ou contacte um administrador.")

        return r
