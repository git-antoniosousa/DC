from odoo import api, models, fields

'''
class Processo(models.Model):
    _name = "gest_diss.processo"
    _description = 'Processo de gestão da dissertação'

    dissertacao = fields.Char('gest_diss.dissertacao', required=True)
    data_homologacao = fields.Date(string="Data de Homologação", required=True)
    estado = fields.Selection([
        ('registado', 'Registado'),
        ('proposta_juri', 'Proposta de Júri'),
        ('homologacao', 'Homologação'),
        ('ata_primeira_reuniao', 'Ata da Primeira Reunião'),
        ('declaracao_aluno', 'Declaração do Aluno'),
        ('ata_prova', 'Ata da Prova'),
        ('registo_nota', 'Registo de Nota'),
        ('aguardar_versao_final', 'A Aguardar Versão Final'),
        ('finalizado', 'Finalizado')
    ], required=True)
    defesa = 
'''