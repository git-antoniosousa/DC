from odoo import api, models, fields
from validate_email import validate_email
from phonenumbers import is_valid_number, parse as parse_number

class Membro(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Arguentes e Docentes'
    _order = 'name'
    _rec_name = 'name'

    categoria = fields.Selection([
        ('prof_auxiliar', 'Professor Auxiliar'),
        ('associado', 'Professor Associado'),
        ('investigador_senior', 'Investigador Sénior'),
        ('investigador_junior', 'Investigador Júnior'),
    ], string='Categoria')

    departamento = fields.Char(string="Departamento")

    tipo_de_membro = fields.Selection([('dc', 'Docente'), ('arg', 'Arguente')], string="Tipo de membro")

    '''
    colocar tag de docente

    variavel_indica se é docente, arguente
    universidade
    escola_faculdade
    departamento
    centro de investigação
    '''



    @api.constrains('phone')
    @api.depends('phone')
    def _check_phone(self):
        for rec in self:
            if rec.phone and not is_valid_number(parse_number(rec.phone, 'PT')):
                raise models.ValidationError(
                    'O número de telefone \'{}\' não é um número português '
                    'válido.'.format(rec.phone))

    @api.constrains('email')
    @api.depends('email')
    def _check_email(self):
        for rec in self:
            if rec.email and not validate_email(rec.email):
                raise models.ValidationError(
                    'O email \'{}\' não é um email válido.'.format(rec.email))