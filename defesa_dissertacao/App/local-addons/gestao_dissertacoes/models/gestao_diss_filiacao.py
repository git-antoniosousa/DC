from odoo import api, models, fields
from validate_email import validate_email
from phonenumbers import is_valid_number, parse as parse_number


class Filiacao(models.Model):
    _name = 'gest_diss.filiacao'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Filiacao dos Arguentes e Docentes'
    _order = 'name'
    _rec_name = 'name'

    partner_id = fields.Many2one('res.partner', required=True, ondelete="cascade")

    filiacao = fields.Many2one('gest_diss.filiacao', 'Filiação')

    name = fields.Char(related='partner_id.name', inherited=True, readonly=False)
    email = fields.Char(related='partner_id.email', inherited=True, readonly=False)
    phone = fields.Char(related='partner_id.mobile', inherited=True, readonly=False)

    tipo_de_filiacao = fields.Selection([('u', 'Universidade'), ('e', 'Empresa'), ('d', 'Departamento'), ('c', 'Centro de Investigação')], string="Tipo de Filiação", default='d', required=True)

#    name = fields.Char(string="Nome")

#    email = fields.Char(string="Email")

    email_facultativo = fields.Char(string="Email Facultativo")

#    phone = fields.Char(string="Número de Contacto")

    website = fields.Char(string="Website")

    street = fields.Char(string="Rua")

    city = fields.Char(string="Cidade")

    zip = fields.Char(string="Zip")


    def tmp_name_get(self):
        if self.name == False:
            return ''
        else:
            return (f"{self.name}, {self.filiacao.tmp_name_get()}")

    def zzname_get(self):
        print(f"name_get {self} {dir(self.env)}")
        ret = list()
        for rec in self:
            ret.append((rec.id, rec.tmp_name_get()))
        print(ret)
        return ret

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