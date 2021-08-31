from odoo import fields, models, api
from odoo.exceptions import ValidationError


class DocFormCandidato(models.TransientModel):
    _name = 'gest_diss.form_candidato_doc'
    _description = 'Formulário do Candidato em como se compromete a não gravação'

    linguagem = fields.Selection([
        ('pt', 'Português'),
        ('eng', 'Inglês'),
    ], string='Linguagem', default='pt', required=True)

    tipo_ficheiro = fields.Selection([
        ('pdf', 'PDF'),
        ('odt', 'Word'),
    ], string='Tipo de Ficheiro', default='pdf', required=True)

    def _default_processos(self):
        return self.env['gest_diss.processo'].browse(self._context.get('active_ids'))

    processos_ids = fields.Many2many('gest_diss.processo', string='Processos', default=_default_processos)

    def gerar_doc(self):

        processos = self._context.get('active_ids')

        for processo in self.processos_ids:
            if processo.estado == 'registo_inicial' or processo.estado == 'correcoes' or processo.estado == 'proposta_juri'\
                    or processo.estado == 'aguardar_confirmacao_juri' or processo.estado == 'aguardar_homologacao':
                raise ValidationError("Não está num estado válido para gerar o Formulário do Candidato em alguns processos! "
                                      "Só pode gerar este formulário após o processo ter sido Homologado!")

        if self.linguagem == 'pt':
            if self.tipo_ficheiro == 'pdf':
                return self.env.ref('gestao_dissertacoes.gerar_form_candidato_pt_report_pdf').report_action(processos)
            else:
                return self.env.ref('gestao_dissertacoes.gerar_form_candidato_pt_report_odt').report_action(processos)
        else:
            if self.tipo_ficheiro == 'pdf':
                return self.env.ref('gestao_dissertacoes.gerar_form_candidato_eng_report_pdf').report_action(processos)
            else:
                return self.env.ref('gestao_dissertacoes.gerar_form_candidato_eng_report_odt').report_action(processos)
