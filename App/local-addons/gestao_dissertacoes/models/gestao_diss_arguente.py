from odoo import api, models, fields


class Arguente(models.Model):
    _name = "gest_diss.arguente"
    _description = 'Arguente'

    nome = fields.Char(string="Nome", required=True)
    entidade_patronal = fields.Char(string="Entidade Patronal", required=True) # ter tabela com empresas?
    cargo = fields.Char(string="Cargo", required=True)
    email = fields.Char(string="Email", required=True)
    contacto_tel = fields.Char(string="Contacto Telefónico")