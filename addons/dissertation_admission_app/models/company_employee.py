from odoo import api, fields, models, exceptions

class CompanyEmployee(models.Model):
    _name = 'dissertation_admission.company_employee'
    _inherits = {'res.users': 'user_id'}
    _description = 'Orientador'
    user_id = fields.Many2one('res.users', ondelete='restrict', required=True)
