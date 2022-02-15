from odoo import api, models, fields
from validate_email import validate_email
from phonenumbers import is_valid_number, parse as parse_number


class Curso(models.Model):
    _name = 'gest_diss.curso'
    _description = 'Cursos'
    _order = 'codigo'
    _rec_name = 'nome'

    codigo = fields.Char(string="Código", required=True)

    nome = fields.Char(string="Nome do Curso", required=True)

    nome_ingles = fields.Char(string="Nome do Curso em Inglês", required=True)

    local = fields.Char(string="Local")

    descricao = fields.Char(string="Descrição")

    #area_cientifica_predominante = fields.Char(string="Área Científica Predominante")
    area_cientifica_predominante = fields.Selection([
        ('Agricultura, Silvicultura e Pescas', 'Agricultura, Silvicultura e Pescas'),
        ('Artes', 'Artes'),
        ('Biotecnologia Agrária e Alimentar ', 'Biotecnologia Agrária e Alimentar '),
        ('Biotecnologia Ambiental', 'Biotecnologia Ambiental'),
        ('Biotecnologia Industrial', 'Biotecnologia Industrial'),
        ('Biotecnologia Médica', 'Biotecnologia Médica'),
        ('Ciência Animal e dos Lacticínios', 'Ciência Animal e dos Lacticínios'),
        ('Ciências Biológicas', 'Ciências Biológicas'),
        ('Ciências da Computação e da Informação ', 'Ciências da Computação e da Informação '),
        ('Ciências da Comunicação', 'Ciências da Comunicação'),
        ('Ciências da Educação', 'Ciências da Educação'),
        ('Ciências da Saúde', 'Ciências da Saúde'),
        ('Ciências da Terra e Ciências do Ambiente ', 'Ciências da Terra e Ciências do Ambiente '),
        ('Ciências Politicas', 'Ciências Politicas'),
        ('Ciências Veterinárias', 'Ciências Veterinárias'),
        ('Direito', 'Direito'),
        ('Economia e Gestão', 'Economia e Gestão'),
        ('Engenharia Civil', 'Engenharia Civil'),
        ('Engenharia do Ambiente', 'Engenharia do Ambiente'),
        ('Engenharia dos Materiais', 'Engenharia dos Materiais'),
        ('Engenharia Eletrotécnica, Eletrónica e Informática', 'Engenharia Eletrotécnica, Eletrónica e Informática'),
        ('Engenharia Mecânica ', 'Engenharia Mecânica '),
        ('Engenharia Médica ', 'Engenharia Médica '),
        ('Engenharia Química ', 'Engenharia Química '),
        ('Filosofia, Ética e Religião ', 'Filosofia, Ética e Religião '),
        ('Física', 'Física'),
        ('Geografia Económica e Social ', 'Geografia Económica e Social '),
        ('História e Arqueologia ', 'História e Arqueologia '),
        ('Línguas e Literaturas Matemática', 'Línguas e Literaturas Matemática'),
        ('Medicina Básica', 'Medicina Básica'),
        ('Medicina Clínica', 'Medicina Clínica'),
        ('Nanotecnologia', 'Nanotecnologia'),
        ('Não Classificado', 'Não Classificado'),
        ('Outras Ciências Agrárias', 'Outras Ciências Agrárias'),
        ('Outras Ciências de Engenharia e Tecnologias ', 'Outras Ciências de Engenharia e Tecnologias '),
        ('Outras Ciências Médicas', 'Outras Ciências Médicas'),
        ('Outras Ciências Naturais ', 'Outras Ciências Naturais '),
        ('Outras Ciências Sociais ', 'Outras Ciências Sociais '),
        ('Outras Humanidades ', 'Outras Humanidades '),
        ('Psicologia', 'Psicologia'),
        ('Química ', 'Química '),
        ('Sociologia', 'Sociologia'),
    ], string ="Área Científica Predominante", readonly=False, default='Electrical, Electronic and Information Engineering')

    phone = fields.Char(string="Número de Contacto")

    email = fields.Char(string="Email")
    email_suporte = fields.Char(string="Email para Suporte")
    email_secretaria = fields.Char(string="Email secretariado")
    website = fields.Char(string="Website")

    contador_ata_id = fields.Many2one('ir.sequence', ondelete="restrict")

    number_next = fields.Integer(related='contador_ata_id.number_next', string="Número da próxima ata", readonly=False, store= False)

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

    def _set_seqnumber(self):
        model = self.env['ir.sequence']
        seq = model.sudo().create(
            {
                'name': f"{self.codigo}_ata_number",
                'prefix': f"{self.codigo}-",
                'padding': 3,
                'suffix': '/%(year)s'
            }
        )
        self.contador_ata_id = seq

    @api.model
    def create(self, values):
        print(f"{values}")
        obj = super(Curso, self).create(values)
        obj._set_seqnumber()
        return obj

    #@api.model
    def write(self, vals):
        if 'number_next' in vals.keys():
            seq = self.env['ir.sequence'].sudo().browse(self.contador_ata_id.id)
            seq.number_next = vals['number_next']
            del vals['number_next']
        return super(Curso, self).write(vals)