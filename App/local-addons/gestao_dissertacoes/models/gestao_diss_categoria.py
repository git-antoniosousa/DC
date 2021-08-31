from odoo import api, models, fields

class Categoria(models.Model):
    _name = 'gest_diss.categoria'
    _description = 'Categoria de membros associados'
    _order = 'nome'
    _rec_name = 'nome'

    nome = fields.Char(string="Nome de Categoria", required=True)

    descricao = fields.Char(string="Descrição")