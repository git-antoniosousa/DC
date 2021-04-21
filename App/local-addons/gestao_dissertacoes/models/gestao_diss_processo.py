from odoo import api, models, fields


class Processo(models.Model):
    _name = "gest_diss.processo"
    _description = 'Processo de gestão da dissertação'

    aluno_id = fields.Many2one('gest_diss.aluno', "Aluno")

    juri_presidente_id = fields.Many2one('gest_diss.docente', 'Presidente')
    juri_vogal1_id = fields.Many2one('gest_diss.docente', 'Vogal 1')
    juri_vogal2_id = fields.Many2one('gest_diss.docente', 'Vogal 2')
    arguente_id = fields.Many2one('gest_diss.arguente', 'Arguente')
    orientador_id = fields.Many2one('gest_diss.docente', 'Orientador')
    coorientador_id = fields.Many2one('gest_diss.docente', 'Co-orientador')
    defesa_id = fields.Many2one('gest_diss.defesa', 'Defesa')

    diss_titulo = fields.Char(string="Título", required=True)
    nota = fields.Integer(string="Nota", required=True)

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

