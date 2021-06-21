from odoo import fields, models, api
from odoo.exceptions import ValidationError


class DocHomologacao(models.TransientModel):
    _name = 'gest_diss.proposta_juri_doc'
    _description = 'Documento de Homologação que contém vários processos'

    curso = None

    tipo_ficheiro = fields.Selection([
        ('pdf', 'PDF'),
        ('odt', 'Word'),
    ], string='Tipo de Ficheiro', default='pdf', required=True)

    def _default_processos(self):
        return self.env['gest_diss.processo'].browse(self._context.get('active_ids'))

    processos_ids = fields.Many2many('gest_diss.processo', string='Processos', default=_default_processos)

    def gerar_doc(self):

        DocHomologacao.curso = self.processos_ids[0].curso.nome

        # Validação do curso e Validação do estado
        curso_1_cod = self.processos_ids[0].curso.codigo
        for processo in self.processos_ids:
            if processo.curso.codigo != curso_1_cod:
                raise ValidationError("Para gerar um conjunto de Propostas de Júri o Curso tem de ser o mesmo em todos os "
                                      "processos!")
            if processo.estado == 'registo_inicial' or processo.estado == 'correcoes':
                raise ValidationError("Não está num estado válido para gerar a Proposta de Júri em alguns processos! "
                                      "Não pode gerar a Proposta de Júri quando está no estado de \"Correções\" ou "
                                      "Registo inicial.")

        if self.tipo_ficheiro == 'pdf':
            return self.env.ref('gestao_dissertacoes.gerar_proposta_juri_report_pdf').report_action(self)
        else:
            return self.env.ref('gestao_dissertacoes.gerar_proposta_juri_report_odt').report_action(self)