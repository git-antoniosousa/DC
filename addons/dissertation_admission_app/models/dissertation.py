from odoo import api, fields, models
from odoo import exceptions


class Dissertation(models.Model):
    states = [
        ('disapproved', 'Reprovado'),
        ('pending', 'Aprovação Pendente'),
        ('approved', 'Aprovado')
    ]
    _name = 'dissertation_admission.dissertation'
    _description = 'Dissertação'

    name = fields.Char('Titulo', required=True)
    description = fields.Text(string='Descrição', required=True)
    state = fields.Selection(states, string='Estado', required=True, default='pending')
    is_public = fields.Boolean(string='Publico?', required=True, default=False)
    course = fields.Many2many('res.company')
    adviser_id = fields.Many2one('res.users', string='Orientador')
    coadviser_id = fields.Many2one('res.users', string='Coorientador')
    student_id = fields.Many2one('res.users', string='Estudante')
    candidates = fields.Many2many('res.users', string='Candidatos', readonly=True)
    reviews = fields.Text(string='Revisão')

#    def read(self, fields):
#        return super(Dissertation, self).read(fields)
