from odoo import api, models, fields
from validate_email import validate_email
from phonenumbers import is_valid_number, parse as parse_number

class Membro(models.Model):
    _name = 'gest_diss.membro'
    _description = 'Arguentes e Docentes'
    _order = 'name'
    _rec_name = 'name'

    categoria = fields.Selection([
        ('prof_auxiliar', 'Professor Auxiliar'),
        ('associado', 'Professor Associado'),
        ('investigador_senior', 'Investigador Sénior'),
        ('investigador_junior', 'Investigador Júnior'),
    ], string='Categoria')

    filiacao_id = fields.Many2one('gest_diss.filiacao', 'Filiacao', domain = "[('tipo_de_filiacao','in',['u', 'e'])]")

    departamento = fields.Many2one('gest_diss.filiacao', 'Departamento', domain = "[('tipo_de_filiacao','=','d')]")

    centro_investigacao = fields.Many2one('gest_diss.filiacao', 'Centro de Investigação', domain = "[('tipo_de_filiacao','=','c')]")

    name = fields.Char(string="Nome")

    phone = fields.Char(string="Número de Contacto")

    email = fields.Char(string="Email")

    email_facultativo = fields.Char(string="Email Facultativo")

    website = fields.Char(string="Website")

    tipo_de_membro = fields.Selection([('dc', 'Docente'), ('arg', 'Arguente')], string="Tipo de membro", default='dc',required=True)

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

    @api.constrains('email_facultativo')
    @api.depends('email_facultativo')
    def _check_email(self):
        for rec in self:
            if rec.email_facultativo and not validate_email(rec.email_facultativo):
                raise models.ValidationError(
                    'O email \'{}\' não é um email válido.'.format(rec.email_facultativo))