from odoo import api, fields, models, exceptions

class CompanyEmployee(models.Model):
    _name = 'dissertation_admission.company_employee'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Funcionario de Empresa'
    partner_id = fields.Many2one('res.partner', ondelete='restrict', required=True)
