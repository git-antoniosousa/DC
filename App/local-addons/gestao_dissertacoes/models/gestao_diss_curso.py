from odoo import api, models, fields
from validate_email import validate_email
from phonenumbers import is_valid_number, parse as parse_number

class Filiacao(models.Model):
    _name = 'gest_diss.curso'
    _description = 'Cursos'
    _order = 'codigo'
    _rec_name = 'codigo'

    codigo = fields.Char(string="Código", required=True)

    nome = fields.Char(string="Nome de Curso", required=True)

    local = fields.Char(string="Local")

    descricao = fields.Char(string="Descrição")

    area_cientifica_predominante = fields.Char(string="Área Científica Predominante")
    
    phone = fields.Char(string="Número de Contacto")

    email = fields.Char(string="Email")

    website = fields.Char(string="Website")

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