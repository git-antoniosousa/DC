from odoo import fields, models, api
from odoo.exceptions import ValidationError


class DocAtaProvas(models.TransientModel):
    _name = 'gest_diss.ata_provas_doc'
    _description = 'Ata das Provas'

    def _default_processos(self):
        return self.env['gest_diss.processo'].browse(self._context.get('active_ids'))

    processos_ids = fields.Many2many('gest_diss.processo', string='Processos', default=_default_processos)

    def gerar_doc(self):

        for processo in self.processos_ids:
            if processo.estado == 'registo_inicial' or processo.estado == 'correcoes' or processo.estado == 'proposta_juri'\
                    or processo.estado == 'aguardar_confirmacao_juri' or processo.estado == 'aguardar_homologacao'\
                    or processo.estado == 'aguardar_homologacao' or processo.estado == 'homologacao' or processo.estado == 'ata_primeira_reuniao'\
                    or processo.estado == 'declaracao_aluno':
                raise ValidationError("Não está num estado válido para gerar a Ata da Prova em alguns processos! "
                                      "Só pode gerar a ata da prova após ter concluído o estado da \"Declaração do Aluno\"")

        processos = self._context.get('active_ids')

        for processo in self.env['gest_diss.processo'].browse(processos):
            print(f"PROCESSO {processo}")
            processo.gera_numero_ata()

        return self.env.ref('gestao_dissertacoes.gerar_ata_provas_report_odt').report_action(processos)