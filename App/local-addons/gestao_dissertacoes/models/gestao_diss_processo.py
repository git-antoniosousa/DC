from typing import DefaultDict
import sys

import werkzeug
import datetime
import calendar, time
import locale
from num2words import num2words
from datetime import datetime
from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError
from odoo.tools.translate import _
from cryptography.fernet import Fernet

# Definir o locale PT
locale.setlocale(locale.LC_ALL, 'pt_PT')

class Processo(models.Model):
    _name = "gest_diss.processo"
    _inherit = ['gest_diss.aluno', 'gest_diss.defesa', 'gest_diss.juri', 'mail.thread']
    _description = 'Processo de gestão da dissertação'

    # --- ano letivo ---
    @api.model
    def _default_ano_letivo(self):
        now = datetime.datetime.now()
        ano = now.year
        mes = now.month
        if mes <= 8: ano -= 1
        return self.env['gest_diss.ano_letivo'].search([('ano_letivo', 'like', str(ano))], limit=1)

    ano_letivo = fields.Many2one('gest_diss.ano_letivo', 'Ano Letivo', default=_default_ano_letivo)

    # --- desativa o trackback ---
    sys.tracebacklimit = 0

    orientador_id = fields.Many2one('gest_diss.membro', 'Orientador')
    coorientador_id = fields.Many2one('gest_diss.membro', 'Co-orientador')

    # --- titulo e nota ---
    diss_titulo = fields.Char(string="Título da Tese")
    nota = fields.Integer(string="Nota")

    # --- homologacao ---
    data_homologacao = fields.Date(string="Data de Homologação")
    data_homologacao_words = fields.Char(string="Data de Homologação por Extenso")

    # --- data primeira reuniao ---
    data_hora_primeira_reuniao = fields.Datetime(string="Data e Hora da Primeira Reunião")
    data_primeira_reuniao_words = fields.Char(string="Data da Primeira Reunião por Extenso")
    hora_primeira_reuniao_words = fields.Char(string="Data da Primeira Reunião por Extenso")

    # --- data primeira reuniao ---
    data_primeira_reuniao = fields.Date(string="Data da Primeira Reunião")

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
    attachment_ids = fields.Many2many('ir.attachment', 'attachment_id', string="Outros Documentos")

    dissertacao = fields.Many2one('ir.attachment', string="Dissertação")

    dissertacao_url = fields.Char(string="URL da Dissertacao")

    # --- verificacao de emails ---
    # true se os convites para o juri foram enviados, false caso contrario
    convites_juri_enviados = fields.Boolean(string="Convites Enviados", default=False)
    # true se a ata da primeira reunião foi enviada, false caso contrario
    primeira_ata_enviada = fields.Boolean(string="Ata da Primeira Reunião", default=False)
    # true se a ata da prova foi enviada, false caso contrario
    ata_prova_enviada = fields.Boolean(string="Ata da Prova", default=False)
    # true se a declaracao do aluno foi enviada, false caso contrario
    declaracao_aluno_enviada = fields.Boolean(string="Declaração do aluno", default=False)

    def write(self, vals):
        if self.estado == 'proposta_juri' and self.data_hora:
            dh = str(self.data_hora).split(" ")
            d = dh[0]
            h = ":".join(dh[1].split(":")[:2])
            vals['data_defesa'] = d
            vals['hora_defesa'] = h
            vals['data_str'] = self.converter_data_para_str(d)
            vals['hora_str'] = h.replace(':', 'h')
            data_words, hora_words = self.converter_data_hora_para_words(str(self.data_hora))
            vals['data_words'] = data_words
            vals['hora_words'] = hora_words
        elif self.estado == 'ata_primeira_reuniao' and self.data_hora_primeira_reuniao:
            data_words, hora_words = self.converter_data_hora_para_words(str(self.data_hora_primeira_reuniao))
            vals['data_primeira_reuniao_words'] = data_words
            vals['hora_primeira_reuniao_words'] = hora_words
        elif self.estado == 'homologacao':
            data_homologacao_words = self.converter_data_para_words(str(self.data_homologacao))
            vals['data_homologacao_words'] = data_homologacao_words
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
        # cria o url da dissertacao
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        full_url = base_url + "/web/content/" + str(self.dissertacao.id) + "?download=true"
        # convites do juri
        self.write({'dissertacao_url': full_url})
        self.link_presidente()
        self.link_arguente()
        self.link_vogal()
        return self.write({'estado': 'aguardar_confirmacao_juri'})

    def undo_prop_juri_action(self):
        return self.write({'estado': 'correcoes'})

    def enviar_convites_juri(self):
        presidente = self.env.ref('gestao_dissertacoes.convite_presidente')
        arguente = self.env.ref('gestao_dissertacoes.convite_arguente')
        vogal = self.env.ref('gestao_dissertacoes.convite_vogal')
        self.message_post_with_template(presidente.id)
        self.message_post_with_template(arguente.id)
        self.message_post_with_template(vogal.id)
        self.write({'convites_juri_enviados': True})

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

    def enviar_ata_primeira_reuniao(self):
        id = None
        for obj in self.attachment_ids:
            if obj.name == "ata-primeira-reuniao.pdf":
                id = obj.id
                break
        if id:
            template_id = self.env.ref('gestao_dissertacoes.ata_primeira_reuniao')
            template_id.attachment_ids = [(4, id)]
            self.message_post_with_template(template_id.id)
            template_id.attachment_ids = [(3, id)]
            self.write({'primeira_ata_enviada': True})
        else:
            raise ValidationError("O ficheiro da ata da primeira reunião não foi encontrado."
                                  " Verifique se o carregou para a plataforma ou se o nome do ficheiro está correto")

    # --- declaracao do aluno ---
    def declaracao_aluno_action(self):
        return self.write({'estado': 'ata_prova'})

    def undo_declaracao_aluno_action(self):
        return self.write({'estado': 'ata_primeira_reuniao'})

    def enviar_declaracao_aluno(self):
        id = None
        for obj in self.attachment_ids:
            if obj.name == "declaracao-aluno.pdf":
                id = obj.id
                break
        if id:
            template_id = self.env.ref('gestao_dissertacoes.declaracao_aluno')
            template_id.attachment_ids = [(4, id)]
            self.message_post_with_template(template_id.id)
            template_id.attachment_ids = [(3, id)]
            self.write({'declaracao_aluno_enviada': True})
        else:
            raise ValidationError("O ficheiro da declaração do aluno não foi encontrado."
                                  " Verifique se o carregou para a plataforma ou se o nome do ficheiro está correto")

    # --- ata da prova ---
    def ata_prova_action(self):
        return self.write({'estado': 'registo_nota'})

    def undo_ata_prova_action(self):
        return self.write({'estado': 'declaracao_aluno'})

    def enviar_ata_prova(self):
        id = None
        for obj in self.attachment_ids:
            if obj.name == "ata-prova.pdf":
                id = obj.id
                break
        if id:
            template_id = self.env.ref('gestao_dissertacoes.ata_prova')
            template_id.attachment_ids = [(4, id)]
            self.message_post_with_template(template_id.id)
            template_id.attachment_ids = [(3, id)]
            self.write({'ata_prova_enviada': True})
        else:
            raise ValidationError("O ficheiro da ata da prova não foi encontrado."
                                  " Verifique se o carregou para a plataforma ou se o nome do ficheiro está correto")

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
        pass

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

    def link_presidente(self):
        key = b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='
        fernet = Fernet(key)
        link = f"p-/-{self._origin.id}-/-{self.juri_presidente_id.name}"
        print(link)
        token = (fernet.encrypt(link.encode())).decode()
        url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/invite/{token}"
        self.write({'convite_presidente_url' : url})

    def link_vogal(self):
        key = b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='
        fernet = Fernet(key)
        link = f"v-/-{self._origin.id}-/-{self.juri_vogal_id.name}"
        print(link)
        token = (fernet.encrypt(link.encode())).decode()
        url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/invite/{token}"
        self.write({'convite_vogal_url' : url})

    def link_arguente(self):
        key = b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='
        fernet = Fernet(key)
        link = f"a-/-{self._origin.id}-/-{self.juri_arguente_id.name}"
        print(link)
        token = (fernet.encrypt(link.encode())).decode()
        url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/invite/{token}"
        self.write({'convite_arguente_url' : url})
        self.write({'convite_arguente_url' : url})

    def converter_data_hora_para_words(self, data_hora):
        date_object = datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")

        ano = num2words(date_object.year, to='year', lang='pt_BR')
        mes = calendar.month_name[date_object.month]
        dia = num2words(date_object.day, to='year', lang='pt_BR')

        hora = num2words(date_object.hour, to='year', lang='pt_BR')
        minuto = num2words(date_object.minute, to='year', lang='pt_BR')

        data_words = dia + ' dias do mês de ' + mes.lower() + ' do ano de ' + ano
        if date_object.minute > 0:
            hora_words = hora + ' horas e ' + minuto + ' minutos'
        else:
            hora_words = hora + ' horas'

        return data_words, hora_words

    def converter_data_para_words(self, data):
        data_object = datetime.strptime(data, "%Y-%m-%d")
        ano = num2words(data_object.year, to='year', lang='pt_BR')
        mes = calendar.month_name[data_object.month]
        dia = num2words(data_object.day, to='year', lang='pt_BR')
        data_words = dia + ' de ' + mes.lower() + ' de ' + ano
        return data_words

    def converter_data_para_str(self, data):
        date_object = datetime.strptime(data, "%Y-%m-%d")
        mes = calendar.month_name[date_object.month]
        data_str = str(date_object.day) + '.' + mes[:3] + '.' + str(date_object.year)
        return data_str
        return data_str
