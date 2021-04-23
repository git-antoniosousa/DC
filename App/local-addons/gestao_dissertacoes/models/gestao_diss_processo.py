from odoo import api, models, fields


class Processo(models.Model):

    _name = "gest_diss.processo"
    _description = 'Processo de gestão da dissertação'
    _rec_name = 'aluno_id'

    dissertacao_id = fields.Many2one('gest_diss.dissertacao', 'Dissertação')
    aluno_id = fields.Many2one('gest_diss.aluno', "Aluno")
    defesa_id = fields.Many2one('gest_diss.defesa', 'Defesa')
    juri_id = fields.Many2one('gest_diss.juri', 'Júri')

    orientador_id = fields.Many2one('gest_diss.docente', 'Orientador')
    coorientador_id = fields.Many2one('gest_diss.docente', 'Co-orientador')

    diss_titulo = fields.Char(string="Título")
    nota = fields.Integer(string="Nota")

    data_homologacao = fields.Date(string="Data de Homologação")
    estado = fields.Selection([
        ('registo_inicial', 'Registo Inicial'),
        ('correcoes', 'Correções'),
        ('registado', 'Registado'),
        ('proposta_juri', 'Proposta de Júri'),
        ('homologacao', 'Homologação'),
        ('ata_primeira_reuniao', 'Ata da Primeira Reunião'),
        ('declaracao_aluno', 'Declaração do Aluno'),
        ('ata_prova', 'Ata da Prova'),
        ('registo_nota', 'Registo de Nota'),
        ('aguardar_versao_final', 'A Aguardar Versão Final'),
        ('finalizado', 'Finalizado')

    ], 'Estado', default="registado")




