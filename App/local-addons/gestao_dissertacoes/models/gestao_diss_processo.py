from odoo import api, models, fields


class Processo(models.Model):
    _name = "gest_diss.processo"
    _description = 'Processo de gestão da dissertação'
    _inherits = {'gest_diss.dissertacao': "dissertacao_id"}

    @api.model
    def _default_processo_stage(self):
        Estado = self.env['gest_diss.processo.estado']
        return Estado.search([], limit=1)

    dissertacao_id = fields.Many2one('gest_diss.dissertacao', 'Dissertação')
    data_homologacao = fields.Date(string="Data de Homologação", required=True)
    estado_id = fields.Many2one(
        'gest_diss.processo.estado',
        default=_default_processo_stage
    )

    def write(self, vals):
        processo = super(Processo, self).write(vals)
        if self.stage_id.book_state:
            self.book_id.state = self.stage_id.book_state
        return processo

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