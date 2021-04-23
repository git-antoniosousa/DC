from odoo import api, models, fields


class Docente(models.Model):
    _name = "gest_diss.docente"
    _description = 'Docente'
    _rec_name = 'nome'


    nome = fields.Char(string="Nome", required=True)
    numero = fields.Char(string="Número", required=True)

    categoria = fields.Selection([
        ('prof_auxiliar', 'Professor Auxiliar'),
        ('associado', 'Professor Associado'),
        ('investigador_senior', 'Investigador Sénior'),
        ('investigador_junior', 'Investigador Júnior'),
    ], string='Categoria')

    '''
    membros do júri tabela
    colocar tag de docente

    variavel_indica se é docente, arguente
    universidade
    escola_faculdade
    departamento
    centro de investigação
    '''




    cargo = fields.Char(string="Cargo", required=True)
    email = fields.Char(string="Email", required=True)
    contacto_tel = fields.Char(string="Contacto Telefónico")