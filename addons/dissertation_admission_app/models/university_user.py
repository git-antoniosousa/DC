from odoo import api, fields, models
from odoo.exceptions import Warning


class UniversityUser(models.Model):
    _inherit = 'res.users'

    university_id = fields.Char('Número Mecanográfico')
    course = fields.Many2many('res.company')
    investigation_center = fields.Char()#fields.Many2one('res.company')
    department = fields.Char()#fields.Many2one('res.company')

#    def _compute_course(self):
#        self.course = self.company_ids
#