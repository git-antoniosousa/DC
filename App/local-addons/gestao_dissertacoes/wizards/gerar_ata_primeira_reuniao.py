from odoo import fields, models, api
from odoo.exceptions import ValidationError


class DocAtaPrimeiraReuniao(models.TransientModel):
    _name = 'gest_diss.ata_primeira_reuniao_doc'
    _description = 'Ata da Primeira Reunião'

    ano = fields.Char(string="Ano da Ata", required=True)

    nr_ultima_ata = fields.Char(string="Número da Última Ata", required=True)

    tipo_ficheiro = fields.Selection([
        ('pdf', 'PDF'),
        ('odt', 'Word'),
    ], string='Tipo de Ficheiro', default='pdf', required=True)

    def _default_processos(self):
        return self.env['gest_diss.processo'].browse(self._context.get('active_ids'))

    processos_ids = fields.Many2many('gest_diss.processo', string='Processos', default=_default_processos)

    def gerar_doc(self):

        # Validação do curso e Validação do estado e validar se vai ser via ZOOM
        for processo in self.processos_ids:
            break

        processos = self._context.get('active_ids')

        if self.tipo_ficheiro == 'pdf':
            return self.env.ref('gestao_dissertacoes.gerar_ata_primeira_reuniao_report_pdf').report_action(processos)
        else:
            return self.env.ref('gestao_dissertacoes.gerar_ata_primeira_reuniao_report_odt').report_action(processos)