from odoo import api, fields, models, exceptions

class Department(models.Model):
    _name = 'dissertation_admission.department'
    _description = 'Departamento'
    name = fields.Char(required=True)
