from odoo import api, models, fields


class Processo(models.Model):

    @api.model
    def _default_processo_stage(self):
        Estado = self.env['gest_diss.processo.estado']
        return Estado.search([], limit=1)

    _name = "gest_diss.processo"
    _description = 'Processo de gestão da dissertação'
    _rec_name = 'aluno_id'
    _inherits = {'gest_diss.aluno':
                     'aluno_id'}

    dissertacao_id = fields.Many2one('gest_diss.dissertacao', 'Dissertação')
    aluno_id = fields.Many2one('gest_diss.aluno', "Aluno")
    defesa_id = fields.Many2one('gest_diss.defesa', 'Defesa')
    juri_id = fields.Many2one('gest_diss.juri', 'Júri')

    orientador_id = fields.Many2one('gest_diss.docente', 'Orientador')
    coorientador_id = fields.Many2one('gest_diss.docente', 'Co-orientador')

    diss_titulo = fields.Char(string="Título")
    nota = fields.Integer(string="Nota")

    data_homologacao = fields.Date(string="Data de Homologação")
    estado_id = fields.Many2one(
        'gest_diss.processo.estado',
        default=_default_processo_stage
    )

    def write(self, vals):
        processo = super(Processo, self).write(vals)
        if self.estado_id.estado:
            self.estado_id.estado = self.estado_id.estado
        return processo

    def confirma_estado(self):
        for rec in self:
            rec.estado_id.estado = 'correcoes'


class ProcessoEstado(models.Model):
    _name = 'gest_diss.processo.estado'
    _order = 'sequence,name'

    name = fields.Char()
    sequence = fields.Integer()
    fold = fields.Boolean()
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


