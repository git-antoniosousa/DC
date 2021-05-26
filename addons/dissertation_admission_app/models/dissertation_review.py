from odoo import api, fields, models


class Review(models.Model):
    _name = 'dissertation_admission.dissertation_review'
    _description = 'Dissertação'

    text = fields.Text(required=True)
    dissertation = fields.Many2one('dissertation_admission.dissertation', required=True
                                   , relation='dissertation_admission_review_dissertation_rel')
