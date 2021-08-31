from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError
import re

class Ano_Letivo(models.Model):
    _name = 'gest_diss.ano_letivo'
    _description = 'Anos Letivos'
    _order = 'ano_letivo'
    _rec_name = 'ano_letivo'

    ano_letivo = fields.Char(string="Ano Letivo", required=True)
    
    descricao = fields.Char(string="Descrição")
    
    @api.constrains('ano_letivo')
    @api.depends('ano_letivo')
    def _check_ano_letivo(self):
        for rec in self:
            if not rec.ano_letivo or (re.match( "^20[0-9]{2}/20[0-9]{2}$", rec.ano_letivo) == None):
                raise models.ValidationError(
                    'O ano letivo \'{}\' não é um ano letivo '
                    'válido.'.format(rec.ano_letivo))