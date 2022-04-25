from odoo import fields, models, api
from odoo.exceptions import ValidationError


class DocJustificacaoArguente(models.TransientModel):
    _name = 'gest_diss.justificacao_arguente_doc'
    _description = 'justificacao_arguente'

    def _default_processos(self):
        return self.env['gest_diss.processo'].browse(self._context.get('active_ids'))

    tipo_ficheiro = fields.Selection([
        ('pdf', 'PDF'),
        ('odt', 'Word'),
    ], string='Tipo de Ficheiro', default='pdf', required=True)

    processos_ids = fields.Many2many('gest_diss.processo', string='Processos', default=_default_processos)

    def gerar_doc(self):

        for processo in self.processos_ids:
            if processo.estado == 'registo_inicial' or processo.estado == 'correcoes' or processo.estado == 'proposta_juri'\
                    or processo.estado == 'aguardar_confirmacao_juri' or processo.estado == 'aguardar_homologacao'\
                    or processo.estado == 'aguardar_homologacao' or processo.estado == 'homologacao' or processo.estado == 'ata_primeira_reuniao'\
                    or processo.estado == 'declaracao_aluno':
                raise ValidationError("Não está num estado válido para gerar a justificacao arguente em alguns processos! "
                                      )

        #processos = self._context.get('active_ids')
        processos = self.processos_ids

        print(f"{self.tipo_ficheiro} {self} {self.env}")
        if self.tipo_ficheiro == 'pdf':
            res = self.env.ref('gestao_dissertacoes.gerar_justificacao_arguente_report_pdf').report_action(processos)
            return res
        else:
            return self.env.ref('gestao_dissertacoes.gerar_justificacao_arguente_report_odt').report_action(processos)