from odoo import fields, models, api
from odoo.exceptions import ValidationError


class DocAtaPrimeiraReuniao(models.TransientModel):
    _name = 'gest_diss.ata_primeira_reuniao_doc'
    _description = 'Ata da Primeira Reunião'


    tipo_ficheiro = fields.Selection([
        ('pdf', 'PDF'),
        ('odt', 'Word'),
    ], string='Tipo de Ficheiro', default='pdf', required=True)

    def _default_processos(self):
        return self.env['gest_diss.processo'].browse(self._context.get('active_ids'))

    processos_ids = fields.Many2many('gest_diss.processo', string='Processos', default=_default_processos)

    def gerar_doc(self):

        for processo in self.processos_ids:
            if processo.estado == 'registo_inicial' or processo.estado == 'correcoes' or processo.estado == 'proposta_juri'\
                    or processo.estado == 'aguardar_confirmacao_juri' or processo.estado == 'aguardar_homologacao'\
                    or processo.estado == 'aguardar_homologacao' or processo.estado == 'homologacao':
                raise ValidationError("Não está num estado válido para gerar a Ata da Primeira Reunião em alguns processos! "
                                      "Só pode gerar esta Ata após ter o processo Homologado!")

        processos = self._context.get('active_ids')

        for processo in self.env['gest_diss.processo'].browse(processos):
            processo.gera_numero_ata1()

        if self.tipo_ficheiro == 'pdf':
            res = self.env.ref('gestao_dissertacoes.gerar_ata_primeira_reuniao_report_pdf').report_action(processos)
            return res
        else:
            return self.env.ref('gestao_dissertacoes.gerar_ata_primeira_reuniao_report_odt').report_action(processos)