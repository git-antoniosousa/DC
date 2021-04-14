from odoo import api, models, fields


class Processo(models.Model):
    _name = "gest_diss.processo"
    _description = 'Processo de gestão da dissertação'

    dissertacao = fields.Char(string="Dissertacao", required=True)
    data_homologacao = fields.Char(string="Título", required=True)
    estado = fields.One2one('gest_diss.aluno', required=True) #seleecionar entre os possiveis
    defesa = fields.One2one('gest_diss.defesa', required=True)
