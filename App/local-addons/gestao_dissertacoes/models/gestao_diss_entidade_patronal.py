from odoo import api, models, fields


class EntidadePatronal(models.Model):
    _name = "gest_diss.entidade_patronal"
    _description = 'Entidade Patronal'

    nome = fields.Char(string="Nome", required=True)
    cidade = fields.Char(string="Cidade", required=True)
    tipo = fields.Selection([('u', 'Universidade'), ('e', 'Empresa')], required=True)