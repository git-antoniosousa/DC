from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _
from cryptography.fernet import Fernet

class Processo(models.Model):
    _name = "gest_diss.processo"
    _inherit = ['gest_diss.aluno', 'gest_diss.defesa', 'gest_diss.juri']
    _description = 'Processo de gestão da dissertação'

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
    ], string='Estado', readonly=True, copy=False, index=True, tracking=3, default='registo_inicial')

    # --- anexar documentos ---
    attachment_ids = fields.Many2many('ir.attachment', 'attachment_id', string="Outros Documentos")

    dissertacao = fields.Many2one('ir.attachment', string="Dissertação")
    # --- wizards de erros ---
    error_filled = {
        'name': 'Mensagem de Erro',
        'type': 'ir.actions.act_window',
        'res_model': 'gest.wizard',
        'view_mode': 'form',
        'target': 'new',
        'flags': {'form': {'action_buttons': False}}
    }

    error_state = {
        'name': 'Mensagem de Erro',
        'type': 'ir.actions.act_window',
        'res_model': 'gest.state_error.wizard',
        'view_mode': 'form',
        'target': 'new',
        'flags': {'form': {'action_buttons': False}}
    }

    # --- ações dos butões dos estados ---
    def registo_aluno_action(self):
        if self.nome and self.numero and self.curso and self.email \
                and self.diss_titulo and self.orientador_id and self.coorientador_id:
            return self.write({'estado': 'correcoes'})
        else:
            return self.error_filled

    def correcoes_action(self):
        if self.estado != 'correcoes':
            return self.error_state
        return self.write({'estado': 'proposta_juri'})

    def prop_juri_action(self):
        if self.estado != 'proposta_juri':
            return self.error_state
        if self.juri_presidente_id and self.juri_vogal_id and self.juri_vogal_id \
                and self.data_hora and self.local and self.sala:
            return self.write({'estado': 'aguardar_confirmacao_juri'})
        else:
            return self.error_filled

    def juri_confirmado_action(self):
        if self.estado != 'aguardar_confirmacao_juri':
            return self.error_state
        return self.write({'estado': 'aguardar_homologacao'})

    def aguardar_homologacao_action(self):
        if self.estado != 'aguardar_homologacao':
            return self.error_state
        return self.write({'estado': 'homologacao'})

    def homologacao_action(self):
        if self.estado != 'homologacao':
            return self.error_state
        if self.data_homologacao:
            return self.write({'estado': 'ata_primeira_reuniao'})
        return self.error_filled

    def ata_primeira_reuniao_action(self):
        if self.estado != 'ata_primeira_reuniao':
            return self.error_state
        return self.write({'estado': 'declaracao_aluno'})

    def declaracao_aluno_action(self):
        if self.estado != 'declaracao_aluno':
            return self.error_state
        return self.write({'estado': 'ata_prova'})

    def ata_prova_action(self):
        if self.estado != 'ata_prova':
            return self.error_state
        return self.write({'estado': 'registo_nota'})

    def registo_nota_action(self):
        if self.estado != 'registo_nota':
            return self.error_state
        if self.nota:
            return self.write({'estado': 'aguardar_versao_final'})
        return self.error_filled

    def aguardar_versao_final_action(self):
        if self.estado != 'aguardar_versao_final':
            return self.error_state
        return self.write({'estado': 'finalizado'})

    def finalizar_action(self):
        if self.estado != 'finalizado':
            return self.error_state

    def desfazer_estado_action(self):
        pass

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
    
    def update_estado(self):
        if self.convite_presidente == 'aceitado' and self.convite_vogal == 'aceitado' and self.convite_arguente == 'aceitado':
            if self.estado == 'aguardar_confirmacao_juri':
                return self.write({'estado': 'aguardar_homologacao'})

    def update_numero_convites_aceites(self):
        num = 0
        if self.convite_presidente == 'aceitado':
            num +=1
        if self.convite_vogal == 'aceitado':
            num +=1
        if self.convite_arguente == 'aceitado':
            num +=1
        self.convites_aceites = num

    def convite(self, resposta, juri):
        print(self.convite_arguente_url)
        print(self.convite_presidente_url)
        print(self.convite_vogal_url)
        if resposta != '':
            if juri == 'p':
                self.write({'convite_presidente': resposta})
            if juri == 'v':
                self.write({'convite_vogal': resposta})
            if juri == 'a':
                self.write({'convite_arguente': resposta})
        self.update_numero_convites_aceites()
        self.update_estado()
        return self

    @api.onchange('juri_presidente_id')
    def link_presidente(self):
        key = b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='
        fernet = Fernet(key)
        link = f"p-/-{self._origin.id}-/-{self.juri_presidente_id.name}"
        print(link)
        token = (fernet.encrypt(link.encode())).decode()
        url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/invite/{token}"
        _my_object = self.env['gest_diss.processo'].sudo().search([('id', 'ilike', self._origin.id)])
        _my_object.write({'convite_presidente_url' : url})
        print(_my_object.convite_presidente_url)

    @api.onchange('juri_vogal_id')
    def link_vogal(self):
        key = b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='
        fernet = Fernet(key)
        link = f"v-/-{self._origin.id}-/-{self.juri_vogal_id.name}"
        print(link)
        token = (fernet.encrypt(link.encode())).decode()
        url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/invite/{token}"
        _my_object = self.env['gest_diss.processo'].sudo().search([('id', 'ilike', self._origin.id)])
        _my_object.write({'convite_vogal_url' : url})
        print(_my_object.convite_vogal_url)

    @api.onchange('juri_arguente_id')
    def link_arguente(self):
        key = b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='
        fernet = Fernet(key)
        link = f"a-/-{self._origin.id}-/-{self.juri_arguente_id.name}"
        print(link)
        token = (fernet.encrypt(link.encode())).decode()
        url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/invite/{token}"
        _my_object = self.env['gest_diss.processo'].sudo().search([('id', 'ilike', self._origin.id)])
        _my_object.write({'convite_arguente_url' : url})
        print(_my_object.convite_arguente_url)
