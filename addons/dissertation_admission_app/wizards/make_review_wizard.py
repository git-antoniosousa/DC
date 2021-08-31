from odoo import models, fields
import logging

class MakeReviewWizard(models.TransientModel):
    _name = 'dissertation_admission.make_review_wizard'

    text = fields.Text(required=True)

    def confirm(self):
        logging.info("Stuff " + str(self._context.get('dissertation')))
        self.env['dissertation_admission.dissertation_review'].sudo().create({
            'dissertation': self._context.get('dissertation'),
            'text': self.text
        })
