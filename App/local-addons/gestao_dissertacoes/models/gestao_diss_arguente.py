from odoo import api, models, fields


class Arguente(models.Model):
    _name = "gest_diss.arguente"
    _description = 'Arguente'
    _rec_name = 'nome'

    nome = fields.Char(string="Nome")
    entidade_patronal = fields.Char(string="Entidade Patronal") # ter tabela com empresas?
    cargo = fields.Char(string="Cargo")
    email = fields.Char(string="Email")
    contacto_tel = fields.Char(string="Contacto Telefónico")