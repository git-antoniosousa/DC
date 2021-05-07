from odoo import api, models, fields
from odoo.odoo.exceptions import ValidationError


class Processo(models.Model):
    _name = "gest_diss.processo"
    _inherit = ['gest_diss.aluno', 'gest_diss.defesa']
    _description = 'Processo de gestão da dissertação'
    # _rec_name = 'aluno_id'

    # aluno_id = fields.Many2one('gest_diss.aluno', "Aluno")

    # curso_filter = fields.Selection(related='aluno_id.curso', store=True)

    # defesa_id = fields.Many2one('gest_diss.defesa', 'Defesa')

    # data_defesa_filter = fields.Datetime(related='defesa_id.data_hora', store=True)

    juri_id = fields.Many2one('gest_diss.juri', 'Júri')

    orientador_id = fields.Many2one('res.partner', 'Orientador')
    coorientador_id = fields.Many2one('res.partner', 'Co-orientador')

    diss_titulo = fields.Char(string="Título da Tese")

    nota = fields.Integer(string="Nota")

    data_homologacao = fields.Date(string="Data de Homologação")

    estado = fields.Selection([
        ('registo_inicial', 'Registo Inicial'),
        ('correcoes', 'Correções'),
        ('proposta_juri', 'Proposta de Júri'),
        ('homologacao', 'Homologação'),
        ('ata_primeira_reuniao', 'Ata da Primeira Reunião'),
        ('declaracao_aluno', 'Declaração do Aluno'),
        ('ata_prova', 'Ata da Prova'),
        ('registo_nota', 'Registo de Nota'),
        ('aguardar_versao_final', 'A Aguardar Versão Final'),
        ('finalizado', 'Finalizado')
    ], string='Estado', readonly=True, copy=False, index=True, tracking=3, default='registo_inicial')

    def registo_aluno_action(self):
        if self.nome and self.numero and self.curso and self.email \
                and self.diss_titulo and self.orientador_id and self.coorientador_id:
            return self.write({'estado': 'correcoes'})

    def correcoes_action(self):
        return self.write({'estado': 'proposta_juri'})

    def prop_juri_action(self):
        return self.write({'estado': 'homologacao'})

    def homologacao_action(self):
        return self.write({'estado': 'ata_primeira_reuniao'})

    def ata_primeira_reuniao_action(self):
        return self.write({'estado': 'declaracao_aluno'})

    def declaracao_aluno_action(self):
        return self.write({'estado': 'ata_prova'})

    def ata_prova_action(self):
        return self.write({'estado': 'registo_nota'})

    def registo_nota_action(self):
        return self.write({'estado': 'aguardar_versao_final'})

    def aguardar_versao_final_action(self):
        return self.write({'estado': 'finalizado'})

    def gerar_edital_action(self):
        x = 10

    def gerar_doc_homologacao_action(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'res_users_report_py3o',
        }

    def enviar_correcoes_action(self):
        pass
