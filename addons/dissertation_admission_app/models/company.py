from odoo import api, fields, models, exceptions
import logging

class Company(models.Model):
    _name = 'dissertation_admission.company'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Empresa'
    partner_id = fields.Many2one('res.partner', ondelete='restrict', required=True)
    employees = fields.Many2many('dissertation_admission.company_employee', compute='_get_employees')

    def _get_employees(self):
        self.employees = self.env['dissertation_admission.company_employee'].sudo()\
            .search([('company_id', '=', self.id)])
