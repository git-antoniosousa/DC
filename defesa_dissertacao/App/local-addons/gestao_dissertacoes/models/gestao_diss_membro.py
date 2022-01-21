from odoo import api, models, fields
from validate_email import validate_email
from phonenumbers import is_valid_number, parse as parse_number

class Membro(models.Model):
    _name = 'gest_diss.membro'
    _description = 'Arguentes e Docentes'
    _inherits =  {'res.partner':'partner_id'}
    _order = 'name'
    _rec_name = 'name'

    categoria = fields.Many2one('gest_diss.categoria', "Categoria", required=True)

    filiacao_id = fields.Many2one('gest_diss.filiacao', 'Afiliação', domain = "[('tipo_de_filiacao','in',['u', 'e'])]")

    departamento = fields.Many2one('gest_diss.filiacao', 'Departamento', domain = "[('tipo_de_filiacao','=','d')]")

    centro_investigacao = fields.Many2one('gest_diss.filiacao', 'Centro de Investigação', domain = "[('tipo_de_filiacao','=','c')]")
    partner_id = fields.Many2one('res.partner', required=True, ondelete="restrict")
    name = fields.Char(related='partner_id.name', inherited=True, readonly=False)
    email = fields.Char(related='partner_id.email', inherited=True, readonly=False)
    phone = fields.Char(related='partner_id.mobile', inherited=True, readonly=False)
    #name = fields.Char(string="Nome")

    #phone = fields.Char(string="Número de Contacto")

    #email = fields.Char(string="Email")

    email_facultativo = fields.Char(string="Email Facultativo")

    website = fields.Char(string="Website")

    tipo_de_membro = fields.Selection([('dc', 'Docente'), ('arg', 'Arguente')], string="Tipo de membro", default='dc',required=True)

    @api.onchange('filiacao_id')
    @api.onchange('departamento')
    @api.onchange('centro_investigacao')
    def compute_filiacao_desc(self):
        for rec in self:
            print(f"compute filiacao desc {rec.name} {rec.centro_investigacao} {rec.departamento.name} {rec.filiacao_id.name}")
            res = ''
            if len(rec.centro_investigacao) != 0:
                res = f"{rec.centro_investigacao.name}; "
            if len(rec.departamento) != 0:
                res = f"{res}{rec.departamento.name}; "
            if len(rec.filiacao_id) != 0:
                res = f"{res}{rec.filiacao_id.name}."
            print(f"compute filiacao desc final {res}.")
            rec.filiacao_desc = res

    filiacao_desc = fields.Char(compute=compute_filiacao_desc, store=False)

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
