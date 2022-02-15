import sys

import calendar
import locale
from num2words import num2words
from datetime import datetime
from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError
from cryptography.fernet import Fernet

# Definir o locale PT
locale.setlocale(locale.LC_ALL, 'pt_PT')

class Processo(models.Model):
    _name = "gest_diss.processo"
    _inherit = ['gest_diss.aluno', 'gest_diss.defesa', 'gest_diss.juri', 'mail.thread']
    _description = 'Processo de gestão da dissertação'
    _order = "data_requerimento desc"
    # --- ano letivo ---
    #@api.constrains('nota')
    def validate_nota(self):
        for rec in self:
            if self.nota < 10 or self.nota >20:
                raise ValidationError("Nota inválida tem de estar entre 10 e 20")
    @api.model
    def _default_ano_letivo(self):
        now = datetime.now()
        ano = now.year
        mes = now.month
        if mes <= 8: return self.env['gest_diss.ano_letivo'].search([('ano_letivo', 'like', f"{ano - 1}/{ano}")], limit=1)
        return self.env['gest_diss.ano_letivo'].search([('ano_letivo', 'like', f"{ano}/{ano + 1}")], limit=1)

    ano_letivo = fields.Many2one('gest_diss.ano_letivo', 'Ano Letivo', default=_default_ano_letivo)

    # --- desativa o trackback ---
    sys.tracebacklimit = 0

    #aluno_id = fields.Many2oneReference()
    orientador_id = fields.Many2one('gest_diss.membro', 'Orientador')
    coorientador_id = fields.Many2one('gest_diss.membro', 'Co-orientador')

    # --- titulo e nota ---
    diss_titulo = fields.Char(string="Título da Tese")
    nota = fields.Integer(string="Nota" )
    pauta = fields.Integer(string="Número de  Pauta")

    # --- pedido de porvas ---

    data_requerimento = fields.Date(string="Data de Requerimento")#, default=datetime.today())

    # --- homologacao ---
    data_homologacao = fields.Date(string="Data de Homologação")
    data_homologacao_words = fields.Char(string="Data de Homologação por Extenso")

    # --- data primeira reuniao ---
    data_hora_primeira_reuniao = fields.Datetime(string="Data e Hora da Primeira Reunião")
    data_primeira_reuniao_words = fields.Char(string="Data da Primeira Reunião por Extenso")
    hora_primeira_reuniao_words = fields.Char(string="Hora da Primeira Reunião por Extenso")

    # --- data primeira reuniao ---
    data_primeira_reuniao = fields.Date(string="Data da Primeira Reunião")
    
    transicoes ={
        '010': ['-' , '030'],
        '030': ['010' , '040'],
        '040': ['030' , '050'],
        '050': ['040' , '060'],
        '060': ['050' , '070'],
        '070': ['060' , '100'],
        '100': ['070' , '110'],
        '110': ['100' , '120'],
        '120': ['110' , '130'],
        '130': ['120' , '140'],
        '140': ['130' , '-'],
    }
    
    estado = fields.Selection([
        ('010', 'Registo Inicial'),
        ('020', 'Correções'),
        ('030', 'Proposta de Júri'),
        ('040', 'Aguardar Confirmação do Júri'),
        ('050', 'Aguardar Homologação'),
        ('060', 'Homolugado'),
        ('070', 'Envio de Convocatória'),
        ('080', 'Ata da Primeira Reunião'),
        ('090', 'Declaração do Aluno'),
        ('100', 'Ata da Prova'),
        ('110', 'Registo de Nota'),
        ('120', 'A Aguardar Versão Final'),
        ('130', 'Lançar Pauta'),
        ('140', 'Finalizado')
    ], string='Estado', readonly=False, copy=False, index=True, tracking=3, default='010')

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
    declaracao_aluno_enviada = fields.Boolean(string="Pedido de anexos enviado", default=False)
    convocatoria_enviada = fields.Boolean(string="Convocatória", default=False)

    nr_ata = fields.Char(string="Numero de ata")
    nr_ata1 = fields.Char(string="Numero da primeira ata")

    def write(self, vals):
        if self.estado == '080' and self.data_hora_primeira_reuniao:
            data_words, hora_words = self.converter_data_hora_para_words(str(self.data_hora_primeira_reuniao))
            vals['data_primeira_reuniao_words'] = data_words
            vals['hora_primeira_reuniao_words'] = hora_words
        elif self.estado == '060' and self.data_homologacao:
            data_homologacao_words = self.converter_data_para_words(str(self.data_homologacao))
            vals['data_homologacao_words'] = data_homologacao_words
        return super(Processo, self).write(vals)

    # --- ações dos butões dos estados ---
    def recuar_action(self):
        for rec in self:
            state = rec.estado
            transicao = self.transicoes[state][0]
            if transicao != '-':
                rec.write({'estado': transicao})
            print(f"RECUAR {state} {self.estado}")
        # return self.write({'estado': '020'})

    def reset_ata(self):
        for rec in self:
            rec.nr_ata = False

    def avancar_action(self):
        for rec in self:
            state = rec.estado
            transicao = self.transicoes[state][1]
            if transicao == '040':
                rec.prop_juri_action()
            if transicao != '-':
                rec.write({'estado': transicao})
            print(f"AVANÇAR  {state} {self.estado}")
        # return self.write({'estado': '020'})


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
        #return self.write({'estado': '040'})


    def enviar_convites_juri(self):
        presidente = self.env.ref('gestao_dissertacoes.convite_presidente')
        arguente = self.env.ref('gestao_dissertacoes.convite_arguente')
        vogal = self.env.ref('gestao_dissertacoes.convite_vogal')
        self.message_post_with_template(presidente.id)
        self.message_post_with_template(arguente.id)
        self.message_post_with_template(vogal.id)
        self.write({'convites_juri_enviados': True})

    #------- convocatoria ----------------

    def enviar_envio_convocatoria(self):
        print(f"ENVIO CONV {self}")
        template_id = self.env.ref('gestao_dissertacoes.envio_convocatoria')
        #self.message_post_with_template(template_id.id)
        for rec in self:
            print(f"REC {rec}")
            composer = self.env['mail.compose.message'].with_context(
                active_id=rec.id,
                active_ids=[rec.id,],
                active_model=rec._name,
                default_composition_mode='mass_mail',
                default_model=rec._name,
                default_res_id=rec.id,
                default_template_id=template_id.id,
                custom_layout=None,
                message_type='notification'
            ).create({
                'composition_mode':'mass_mail',
                'message_type': 'notification'
            })
            update_values = composer.onchange_template_id(template_id.id,'mass_mail', rec._name, rec.id)['value']
            composer.write(update_values)
            update_values = composer.render_message(rec.id)
            if rec.juri_presidente_id.email == False or rec.juri_arguente_id.email == False\
                or rec.juri_vogal_id.email == False or rec.email == False or \
                    rec.juri_presidente_id.email == '' or rec.juri_arguente_id.email == '' \
                    or rec.juri_vogal_id.email == '' or rec.email == '':
                raise ValidationError("Um dos elementos do juri ou o aluno não têm email atribuído")

            mail_to = f"{rec.juri_presidente_id.email},{rec.juri_arguente_id.email},{rec.juri_vogal_id.email},{rec.email}"
            mail_cc = f"{rec.curso.email}"
            if rec.curso.email_suporte != False:
                mail_cc = f"{mail_cc},{rec.curso.email_suporte}"
            mailer = self.env['mail.mail'].sudo().create(
                {
                    'email_to': mail_to,
                    'email_cc': mail_cc,
                    'subject': update_values['subject'],
                    'body_html': update_values['body'],
                }
            )
            mailer.send()
            print(f"{update_values['subject']} {update_values['body']}")
            self.write({'convocatoria_enviada': True})

    # --- ata primeira reuniao ---

    def enviar_ata_primeira_reuniao(self):
        id = None
        for obj in self.attachment_ids:
            if obj.name.split('.')[0] == "ata-primeira-reuniao":
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

    def gera_numero_ata(self):
        print(f"gera_numero_ata {self.nr_ata}")
        data = dict()
        if self.nr_ata == False:
            print(f"{self.curso.contador_ata_id.id}")
            data['nr_ata'] = self.env['ir.sequence'].get_id(self.curso.contador_ata_id.id)
            #data['nr_ata'] = self.env['ir.sequence'].next_by_code('gestao_dissertacoes.atanumber')
            self.write(data)

    def gera_numero_ata1(self):
        print(f"gera_numero_ata1 {self.nr_ata1}")
        data = dict()
        if self.nr_ata1 == False:
            data['nr_ata1'] = self.env['ir.sequence'].next_by_code('gestao_dissertacoes.ata1number')
            self.write(data)

    # --- declaracao do aluno ---

    def enviar_declaracao_aluno(self):
        id = None
        for obj in self.attachment_ids:
            if obj.name.split('.')[0] == "declaracao-aluno":
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

    def enviar_pedido_anexos(self):
        if self.nota < 10 or self.nota > 20:
            raise ValidationError(f"A nota tem de ser entre 10 e 20. É {self.nota}.")
        template_id = self.env.ref('gestao_dissertacoes.pedido_anexos')
        self.message_post_with_template(template_id.id)
        self.write({'declaracao_aluno_enviada': True})

    # --- ata da prova ---


    def enviar_ata_prova(self):
        id = None
        attach_name =''
        for obj in self.attachment_ids:
            if self.nr_ata == False:
                raise ValidationError("Nao foi encontrado numero de ata. Gere a ata das provas")

            if obj.name == f"Provas-{self.nr_ata.replace('/','-')}-{self.name}.odt":
                id = obj.id
                attach_name = f"Provas-{self.nr_ata.replace('/','-')}-{self.name}.odt"
                break
        if id:
            template_id = self.env.ref('gestao_dissertacoes.ata_prova')
            template_id.attachment_ids = [(4, id)]
            self.message_post_with_template(template_id.id)
            template_id.attachment_ids = [(3, id)]
            self.write({'ata_prova_enviada': True})
        else:
            raise ValidationError(f"O ficheiro da ata da prova não foi encontrado.\n Verifique se o carregou para a plataforma ou se o nome({attach_name}) do ficheiro está correto")

    # --- registo da nota ---

    # --- aguardar versao final ---

    # --- lancar pauta ---

    # --- finalizar ---

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
            if self.estado == '040':
                return self.write({'estado': '050'})

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

    def gera_link_vc(self):
        key = b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='
        fernet = Fernet(key)
        link = f"linkvc-/-{self.id}-/-{self.name}"
        print(link)
        token = (fernet.encrypt(link.encode())).decode()
        url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/linkvc/{token}"
        self.write({'link_vc_url': url})
        print(f"ENVIO PEDIDO LINK VC {self}")
        template_id = self.env.ref('gestao_dissertacoes.envio_pedido_link')
        self.message_post_with_template(template_id.id)


    def update_link_vc(self, resposta):
        if resposta != '':
            self.write({'link_vc': resposta})
        return self

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
