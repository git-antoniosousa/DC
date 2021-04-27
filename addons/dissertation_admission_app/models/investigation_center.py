from odoo import api, fields, models, exceptions

class InvestigationCenter(models.Model):
    _name = 'dissertation_admission.investigation_center'
    _description = 'Centro de Investigação'

    name = fields.Char(required=True)
