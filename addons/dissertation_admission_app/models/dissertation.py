from odoo import api, fields, models
from odoo.exceptions import Warning

class Dissertation(models.Model):
    _name = 'dissertation_admission.dissertation'
    _description = 'Dissertação'

    name = fields.Char('Titulo', required=True)
    description = fields.Text('Descrição', required=True)
    public = fields.Boolean('Ativo', default=False)
    date_published = fields.Date('Data de criação')
    publisher_id = fields.Many2one('res.partner', string='Autor')
    adviser_id = fields.Many2one('res.partner', string='Orientador')
    coadviser_id = fields.Many2one('res.partner', string='Coorientador')
    student_id = fields.Many2one('res.partner', string='Estudante')
    
