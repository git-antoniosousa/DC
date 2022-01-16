from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _sql_constraints = [
        ('email_uniq', 'UNIQUE(email)', 'Já existe um contacto com esse email')
    ]
    @api.constrains('email')
    def _check_email(self):
        model = self.env['res.partner']
        for record in self:
            res = model.search([('email', '=' , record.email)])
            print(f"{res}")
            if len(res) != 1:
                print(f"{res} {res[0].email}")
                raise ValidationError(_('Já existe um contacto com este email'))
