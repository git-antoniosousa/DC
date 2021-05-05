from odoo import api, fields, models, exceptions

class Company(models.Model):
    _name = 'dissertation_admission.company'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Secretaria de Curso'
    partner_id = fields.Many2one('res.partner', ondelete='restrict', required=True)
