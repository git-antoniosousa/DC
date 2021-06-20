import werkzeug

from odoo import api, models, fields
from odoo.odoo import exceptions
import sys


class Processo(models.Model):
    _name = "gest_diss.processo"
    _inherit = ['gest_diss.aluno', 'gest_diss.defesa', 'gest_diss.juri', 'mail.thread']
    _description = 'Processo de gestão da dissertação'

    # --- desativa o trackback ---
    sys.tracebacklimit = 0

    orientador_id = fields.Many2one('gest_diss.membro', 'Orientador')
    coorientador_id = fields.Many2one('gest_diss.membro', 'Co-orientador')

    # --- titulo e nota ---
    diss_titulo = fields.Char(string="Título da Tese")
    nota = fields.Integer(string="Nota")

    # --- homologacao ---
    data_homologacao = fields.Date(string="Data de Homologação")

    # --- estados do processo ---
    estado = fields.Selection([
        ('registo_inicial', 'Registo Inicial'),
        ('correcoes', 'Correções'),
        ('proposta_juri', 'Proposta de Júri'),
        ('aguardar_confirmacao_juri', 'Aguardar Confirmação do Júri'),
        ('aguardar_homologacao', 'Aguardar Homologação'),
        ('homologacao', 'Homologação'),
        ('ata_primeira_reuniao', 'Ata da Primeira Reunião'),
        ('declaracao_aluno', 'Declaração do Aluno'),
        ('ata_prova', 'Ata da Prova'),
        ('registo_nota', 'Registo de Nota'),
        ('aguardar_versao_final', 'A Aguardar Versão Final'),
        ('finalizado', 'Finalizado')
    ], string='Estado', readonly=False, copy=False, index=True, tracking=3, default='registo_inicial')

    # --- anexar documentos ---
    attachment_ids = fields.Many2many('ir.attachment', 'attachment_id', string="Documentos")

    # --- verificacao de emails ---
    # true se os convites para o juri foram enviados, false caso contrario
    convites_juri_enviados = fields.Boolean(string="Convites Enviados", default=False)

    # --- wizards de erros ---
    error_state = {
        'name': 'Mensagem de Erro',
        'type': 'ir.actions.act_window',
        'res_model': 'gest.state_error.wizard',
        'view_mode': 'form',
        'target': 'new',
        'flags': {'form': {'action_buttons': False}}
    }

    def send_email(self):
        # verificar se o url de callback já existe, só depois enviar email
        # ou verificar se ao carregar no botao de enviar email, todos os campos desse estado estao preenchidos
        # template_id = self.env.ref('gestao_dissertacoes.convite_presidente')
        # self.message_post_with_template(template_id.id)
        self.write({'convites_juri_enviados': 'sim'})

    def write(self, vals):
        if self.estado == 'proposta_juri' and self.data_hora:
            dh = str(self.data_hora).split(" ")
            d = dh[0]
            h = ":".join(dh[1].split(":")[:2])
            vals['data_defesa'] = d
            vals['hora_defesa'] = h
        return super(Processo, self).write(vals)

    # --- ações dos butões dos estados ---
    def registo_aluno_action(self):
        return self.write({'estado': 'correcoes'})

    # --- correções ---
    def correcoes_action(self):
        return self.write({'estado': 'proposta_juri'})

    def undo_correcoes_action(self):
        return self.write({'estado': 'registo_inicial'})

    # --- proposta do juri ---
    def prop_juri_action(self):
        return self.write({'estado': 'aguardar_confirmacao_juri'})

    def undo_prop_juri_action(self):
        return self.write({'estado': 'correcoes'})

    # --- confirmação do juri ---
    def juri_confirmado_action(self):
        return self.write({'estado': 'aguardar_homologacao'})

    def undo_juri_confirmado_action(self):
        return self.write({'estado': 'proposta_juri'})

    # --- aguardar homologacao ---
    def aguardar_homologacao_action(self):
        return self.write({'estado': 'homologacao'})

    def undo_aguardar_homologacao_action(self):
        return self.write({'estado': 'aguardar_confirmacao_juri'})

    # --- homologacaco ---
    def homologacao_action(self):
        return self.write({'estado': 'ata_primeira_reuniao'})

    def undo_homologacao_action(self):
        return self.write({'estado': 'aguardar_homologacao'})

    # --- ata primeira reuniao ---
    def ata_primeira_reuniao_action(self):
        return self.write({'estado': 'declaracao_aluno'})

    def undo_ata_primeira_reuniao_action(self):
        return self.write({'estado': 'homologacao'})

    # --- declaracao do aluno ---
    def declaracao_aluno_action(self):
        return self.write({'estado': 'ata_prova'})

    def undo_declaracao_aluno_action(self):
        return self.write({'estado': 'ata_primeira_reuniao'})

    # --- ata da prova ---
    def ata_prova_action(self):
        return self.write({'estado': 'registo_nota'})

    def undo_ata_prova_action(self):
        return self.write({'estado': 'declaracao_aluno'})

    # --- registo da nota ---
    def registo_nota_action(self):
        return self.write({'estado': 'aguardar_versao_final'})

    def undo_registo_nota_action(self):
        return self.write({'estado': 'ata_prova'})

    # --- aguardar versao final ---
    def aguardar_versao_final_action(self):
        return self.write({'estado': 'finalizado'})

    def undo_aguardar_versao_final_action(self):
        return self.write({'estado': 'registo_nota'})

    # --- finalizar ---
    def finalizar_action(self):
        if self.estado != 'finalizado':
            return self.error_state

    def undo_finalizar_action(self):
        return self.write({'estado': 'aguardar_versao_final'})

    # --- ---
    def gerar_edital_action(self):
        pass

    def gerar_doc_homologacao_action(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'res_users_report_py3o',
        }

    def enviar_correcoes_action(self):
        pass

