from odoo import models, fields
import logging

class MakeReviewWizard(models.TransientModel):
    _name = 'dissertation_admission.make_review_wizard'
    _description = 'Make revision wizard'
    text = fields.Text(required=True)

    def confirm(self):
        logging.info("Stuff " + str(self._context.get('dissertation')))
        self.env['dissertation_admission.dissertation_review'].sudo().create({
            'dissertation': self._context.get('dissertation'),
            'text': self.text
        })
        tema = self._context.get('dissertation')
        info = self.env['dissertation_admission.dissertation'].browse(tema)
        email  = info.create_uid.login
        #print(f"EMAIL : {email} {info} {info.create_uid.login}")
        mail_to = f"{email}"
        mail_cc = f"dcmei@di.uminho.pt"
        mailer = self.env['mail.mail'].sudo().create(
                 {
                     'email_to': mail_to,
                     'email_cc': mail_cc,
                     'subject': f"tema: {info.name}",
                     'body_html': f"<p>Caro {info.create_uid.name}</p><p>{self.text}</p>",
                 }
             )
        mailer.send()
