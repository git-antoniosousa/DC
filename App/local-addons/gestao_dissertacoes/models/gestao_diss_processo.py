from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _

class Processo(models.Model):
    _name = "gest_diss.processo"
    _inherit = ['gest_diss.aluno', 'gest_diss.defesa', 'gest_diss.juri']
    _description = 'Processo de gestão da dissertação'

    orientador_id = fields.Many2one('gest_diss.membro', 'Orientador')
    coorientador_id = fields.Many2one('gest_diss.membro', 'Co-orientador')

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
        else:
            return {
                'name': 'Mensagem de Erro',
                'type': 'ir.actions.act_window',
                'res_model': 'gest.wizard',
                'view_mode': 'form',
                #'view_type': 'form',
                'target': 'new',
                'flags': {'form': {'action_buttons': False}}
            }

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

    def finalizar_action(self):
        pass

    def gerar_edital_action(self):
        pass

    def gerar_doc_homologacao_action(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'res_users_report_py3o',
        }

    def enviar_correcoes_action(self):
        pass
