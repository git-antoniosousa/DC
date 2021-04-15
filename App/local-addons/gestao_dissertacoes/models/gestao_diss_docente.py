from odoo import api, models, fields


class Docente(models.Model):
    _name = "gest_diss.docente"
    _description = 'Docente'

    nome = fields.Char(string="Nome", required=True)
    numero = fields.Char(string="Número", required=True)
    cargo = fields.Char(string="Cargo", required=True)
    email = fields.Char(string="Email", required=True)
    contacto_tel = fields.Char(string="Contacto Telefónico")