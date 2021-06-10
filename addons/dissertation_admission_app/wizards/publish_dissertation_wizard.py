from odoo import models, fields
import logging

class PublishDissertationWizard(models.TransientModel):
    _name = 'dissertation_admission.publish_dissertation_wizard'
    dissertations = fields.Many2many('dissertation_admission.dissertation'
                                     , relation='dissertation_admission_dissertation_publish_wizard_rel')

    def confirm(self):
        for dissertation in self.dissertations:
            dissertation.publish()
