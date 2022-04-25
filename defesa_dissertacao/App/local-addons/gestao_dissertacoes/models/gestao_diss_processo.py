import os
import sys

import calendar
import locale
import base64
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from contextlib import closing
from num2words import num2words
from datetime import datetime
from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError
from cryptography.fernet import Fernet
import tempfile

import pytz
# Definir o locale PT
locale.setlocale(locale.LC_ALL, 'pt_PT')

class Processo(models.Model):
    _name = "gest_diss.processo"
    _inherit = ['gest_diss.aluno', 'gest_diss.defesa', 'gest_diss.juri', 'mail.thread']
    _description = 'Processo de gestão da dissertação'
    _order = "data_hora asc, data_requerimento asc"
    # --- ano letivo ---
    @api.constrains('nota')
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

    @api.depends('nota')
    def _compute_cnota(self):
        print(f"Compute CNOTA {self}")
        for obj in self:
            print(f" Process Compute NOTA {obj}")
            obj.enviar_pedido_anexos()
            obj.enviar_pedido_assinatura_decl_arguente()
            obj.avancar_action()

    cnota = fields.Boolean(compute='_compute_cnota', store = True)

    # --- pedido de provas ---

    data_requerimento = fields.Date(string="Data de Requerimento")#, default=datetime.today())

    # --- homologacao ---
    data_homologacao = fields.Date(string="Data de Homologação")

    @api.depends('data_homologacao')
    def data_homolugacao_para_words(self):
        print(f"data_homolugacao_para_words {self}")
        data_words = dict()
        for rec in self:
            #data_object = datetime.strptime(rec.data_homologacao, "%Y-%m-%d")
            data_object = rec.data_homologacao
            ano = num2words(data_object.year, to='year', lang='pt_PT')
            mes = calendar.month_name[data_object.month]
            dia = num2words(data_object.day, to='year', lang='pt_PT')
            data_words[rec.id] = dia + ' de ' + mes.lower() + ' de ' + ano
            rec.data_homologacao_words = dia + ' de ' + mes.lower() + ' de ' + ano
        print(f"data_homolugacao_para_words {data_words}")
        return data_words


    data_homologacao_words = fields.Char(compute = 'data_homolugacao_para_words', string="Data de Homologação por Extenso")

    data_hora_primeira_reuniao = fields.Datetime(string="Data e Hora da Primeira Reunião")

    @api.depends('data_hora_primeira_reuniao')
    def data_hora_para_words(self, data_hora_primeira_reuniao):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for rec in self:
            date_object = rec.data_hora_primeira_reuniao.astimezone(local) #datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")

            ano = num2words(date_object.year, to='year', lang='pt_PT')
            mes = calendar.month_name[date_object.month]
            dia = num2words(date_object.day, to='year', lang='pt_PT')

            hora = num2words(date_object.hour, to='year', lang='pt_PT')
            minuto = num2words(date_object.minute, to='year', lang='pt_PT')

            data_words = dia + ' dias do mês de ' + mes.lower() + ' do ano de ' + ano
            if date_object.minute > 0:
                hora_words = hora + ' horas e ' + minuto + ' minutos'
            else:
                hora_words = hora + ' horas'
            rec.data_primeira_reuniao_words = data_words
            rec.hora_primeira_reuniao_words = hora_words
            return data_words, hora_words
    # --- data primeira reuniao ---

    data_primeira_reuniao_words = fields.Char(compute = 'data_hora_para_words', string="Data da Primeira Reunião por Extenso")
    hora_primeira_reuniao_words = fields.Char(compute = 'data_hora_para_words', string="Hora da Primeira Reunião por Extenso")

    # --- data primeira reuniao ---
    data_primeira_reuniao = fields.Date(string="Data da Primeira Reunião")
    
    transicoes ={
        '010': ['-' , '030'],
        '030': ['010' , '040'],
        '040': ['030' , '050'],
        '050': ['040' , '060'],
        '060': ['050' , '070'],
        '070': ['060' , '075'],
        '075': ['070', '100'],
        '100': ['070' , '110'],
        '110': ['100' , '120'],
        '120': ['110' , '125'],
        '125': ['120', '130'],
        '130': ['125' , '140'],
        '140': ['130' , '-'],
    }
    
    estado = fields.Selection([
        ('010', 'Registo Inicial'),
        ('020', 'Correções'),
        ('030', 'Proposta de Júri'),
        ('040', 'Aguardar Confirmação do Júri'),
        ('050', 'Aguardar Homologação'),
        ('060', 'Homologado'),
        ('070', 'Envio de Convocatória'),
        ('075', 'Convocatória Confirmada'),
        #('080', 'Ata da Primeira Reunião'),
        #('090', 'Declaração do Aluno'),
        ('100', 'Ata da Prova'),
        ('110', 'Registo de Nota'),
        ('120', 'A Aguardar Versão Final'),
        ('125', 'Validar Versão Final/Anexos'),
        ('130', 'Lançar Pauta'),
        ('140', 'Finalizado')
    ], string='Estado', readonly=False, copy=False, index=True, tracking=3, default='010')

    # --- anexar documentos ---
    attachment_ids = fields.Many2many('ir.attachment', 'attachment_id', string="Outros Documentos")

    dissertacao = fields.Many2one('ir.attachment', string="Dissertação")
    ata_assinada = fields.Many2one('ir.attachment', string="Ata das Provas")
    atualizacao_diss = fields.Boolean(string="Necessita Atualizações", default=False)
    dissertacao_final = fields.Many2one('ir.attachment', string="Dissertação final")
    anexo5a = fields.Many2one('ir.attachment', string="Anexo 5A")
    anexos_url = fields.Char(string="URL Anexos")
    anexo5b = fields.Many2one('ir.attachment', string="Anexo 5B")
    enviar_decl_arguente = fields.Boolean(string="Enviar Declaração participação", default=False)
    decl_arguente_url = fields.Char(string="URL declaração arguente")
    decl_arguente = fields.Many2one('ir.attachment', string="declaração arguente")
    decl_arguente_assinada_enviada = fields.Boolean(string="Declaração arguente enviada", default=False)
    decl_arguente_enviada = fields.Boolean(string="Pedido assinatura de declaração arguente enviada", default=False)
    dissertacao_url = fields.Char(string="URL da Dissertacao")
    nota_url = fields.Char(string="URL da Nota")

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

    convocatoria_presidente_url  = fields.Char(string="Link Convocatória Presidente Júri")
    convocatoria_arguente_url = fields.Char(string="Link Convocatória Arguente Júri")
    convocatoria_vogal_url = fields.Char(string="Link Convocatória Vogal Júri")
    convocatoria_aluno_url = fields.Char(string="Link Convocatória Aluno")
    convocatoria_presidente = fields.Boolean(string="Confirmação Presidente Júri")
    convocatoria_arguente = fields.Boolean(string="Confirmação Arguente Júri")
    convocatoria_vogal = fields.Boolean(string="Confirmação Vogal Júri")
    convocatoria_aluno = fields.Boolean(string="Confirmação Aluno")
    numero_convites_convocatoria = fields.Integer(string="Convocatorias Aceites", default=0)

    nr_ata = fields.Char(string="Numero de ata")
    nr_ata1 = fields.Char(string="Numero da primeira ata")

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
            print(f"avancar_action {rec.estado} {transicao} {rec.numero_convites_convocatoria}")
            if transicao == '040':
                rec.prop_juri_action()
            if transicao == '070':
                if rec.numero_convites_convocatoria == 4:
                    transicao = self.transicoes[transicao][1]
            if state == '125':
                print(f"VALIDAR {rec.anexo5a.id} {rec.anexo5b.id} {rec.atualizacao_diss} {rec.dissertacao_final.id}")
                if rec.anexo5a.id == False or\
                    rec.anexo5b.id == False or \
                    (rec.atualizacao_diss == True and rec.dissertacao_final.id == False):
                    raise ValidationError("Falta versão final da tese ou anexos")

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

    def gerar_links_convocatoria(self):
        key = bytes(self.env['ir.config_parameter'].sudo().get_param('gest_diss.fernet_key',
                                                                     'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='),
                    'utf-8')
        fernet = Fernet(key)
        data =[('presidente','cp'), ('arguente', 'ca'), ('vogal','cv'), ('aluno', 'cal')]
        for k,v in data:
            if eval(f"self.convocatoria_{k}_url") ==False:
                now = datetime.now()
                link = f"{v}-/-{self.id}-/-{self.name}-/-{now}"
                print(link)
                token = (fernet.encrypt(link.encode())).decode()
                url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/convocatoria/{token}"
                self.write({f'convocatoria_{k}_url' : url})


    def enviar_envio_convocatoria(self):
        print(f"ENVIO CONV {self}")
        template_id = self.env.ref('gestao_dissertacoes.envio_convocatoria')
        #self.message_post_with_template(template_id.id)
        for rec in self:
            print(f"Gerar links {rec}")
            rec.gerar_links_convocatoria()
            data = [('presidente', 'cp'), ('arguente', 'ca'), ('vogal', 'cv'), ('aluno', 'cal')]

            for k,v in data:
                print(f"envir {k}")
                template_id = self.env.ref(f'gestao_dissertacoes.convocatoria_{k}')
                rec.message_post_with_template(template_id.id)
            rec.write({'convocatoria_enviada': True})

    def enviar_envio_convocatoria_old(self):
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
        print(f"enviar_pedido_anexos {self}")
        for obj in self:
            if obj.declaracao_aluno_enviada == False:
                if obj.nota == 0:
                    continue
                if obj.nota < 10 or obj.nota > 20:
                    raise ValidationError(f"A nota tem de ser entre 10 e 20. É {obj.nota}.")
    
                obj.gera_link_anexos()
                if len(obj.coorientador_id) != 0:
                    orientador = f"{obj.orientador_id.name}, {obj.coorientador_id.name}"
                else:
                    orientador = f"{obj.orientador_id.name}"
                now = datetime.now()
                fields5a = {
                    'Nome': obj.name,
                    'email': obj.email,
                    #'Text3': "omeu telefone",
                    #'CC': "o meu CC",
                    'Check Box5': 'Yes',
                    'Titulo': obj.diss_titulo,
                    'Text7': orientador,
                    'Text9': obj.data_hora.strftime('%d-%m-%Y'),
                    'Text11': obj.curso.nome,
                    'Check Box17': 'Yes',
                    'Text14': now.strftime('%d'),
                    'Text15': now.strftime('%m'),
                    'Text16': now.strftime('%Y'),
                    # pag 2 5B
                    'Text34': obj.name,
                    'Check Box26': 'Yes',
                    'Text35': obj.diss_titulo,
                    'Text4': orientador,
                    'Text37': obj.data_hora.strftime('%d-%m-%Y'),
                    'Text39': obj.curso.nome,
                    'UOEIS': 'Escola de Engenharia',
                    'Text41': obj.curso.departamento,
                    'FOS': obj.curso.area_cientifica_predominante,
                    'Text45': obj.curso.ECTS_diss,
                    'Text46': obj.nota,
                }
    
    
                fda, fnamea = tempfile.mkstemp(suffix=".pdf", prefix="Anexo5A.")
                fdb, fnameb = tempfile.mkstemp(suffix=".pdf", prefix="Anexo5B.")
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
                anexo5a = f"{path}/../templates/Anexo5AeB.PDF"
    
                writer1 = PyPDF2.PdfFileWriter()
                writer2 = PyPDF2.PdfFileWriter()
    
                with closing(open(anexo5a, 'rb')) as infile:
                    reader = PyPDF2.PdfFileReader(infile, strict=False)
                    writer1.addPage(reader.getPage(0))
                    writer2.addPage(reader.getPage(1))
                    writer1.updatePageFormFieldValues(writer1.getPage(0), fields5a)
                    writer2.updatePageFormFieldValues(writer2.getPage(0), fields5a)
    
                    with closing(os.fdopen(fda, 'wb')) as outfile:
                        writer1.write(outfile)
    
                    with closing(open(fnamea, 'rb')) as infile:
                        data1 = infile.read()
                        vals = {
                            'res_model': obj._name,
                            'res_id': obj.id,
                            'datas': base64.b64encode(data1),
                            'name': "Anexo5A.pdf",
                            'mimetype': 'application/pdf',
                        }
                        at_id1 = obj.env['ir.attachment'].create(vals)
                        obj.write({'attachment_ids': [(4, at_id1.id)]})
    
                    with closing(os.fdopen(fdb, 'wb')) as outfile:
                        writer2.write(outfile)
    
                    with closing(open(fnameb, 'rb')) as infile:
                        data1 = infile.read()
                        vals = {
                            'res_model': obj._name,
                            'res_id': obj.id,
                            'datas': base64.b64encode(data1),
                            'name': "Anexo5B.pdf",
                            'mimetype': 'application/pdf',
                        }
                        at_id2 = obj.env['ir.attachment'].create(vals)
                        obj.write({'attachment_ids': [(4, at_id2.id)]})
    
                    os.unlink(fnamea)
                    os.unlink(fnameb)
                    print(f"PATH {os.path} {os.curdir} {os.getcwd()} {path}")
    
    
                template_id = obj.env.ref('gestao_dissertacoes.pedido_anexos')
                template_id.attachment_ids = [(4, at_id1.id)]
                template_id.attachment_ids = [(4, at_id2.id)]
                obj.message_post_with_template(template_id.id)
                template_id.attachment_ids = [(3, at_id1.id)]
                template_id.attachment_ids = [(3, at_id2.id)]
                obj.write({'declaracao_aluno_enviada': True})

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
        if id and self.ata_prova_enviada == False:
            self.gera_link_nota()
            template_id = self.env.ref('gestao_dissertacoes.ata_prova')
            template_id.attachment_ids = [(4, id)]
            self.message_post_with_template(template_id.id)
            template_id.attachment_ids = [(3, id)]
            self.write({'ata_prova_enviada': True})
            if self.estado == '100':
                self.avancar_action()
        else:
            if self.ata_prova_enviada == True:
                raise ValidationError(f"A ata da prova já foi enviada")
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
        if self.estado == '040':
            if self.convite_presidente == 'aceitado' and self.convite_vogal == 'aceitado' and self.convite_arguente == 'aceitado':
                return self.write({'estado': '050'})
        if self.estado == '070':
            if self.numero_convites_convocatoria == 4:
                return self.write({'estado': self.transicoes['070'][1]})

    def update_numero_convites_aceites(self):
        num = 0
        if self.convite_presidente == 'aceitado':
            num +=1
        if self.convite_vogal == 'aceitado':
            num +=1
        if self.convite_arguente == 'aceitado':
            num +=1
        self.convites_aceites = num

    @api.depends('convocatoria_presidente', 'convocatoria_vogal', 'convocatoria_arguente', 'convocatoria_aluno')
    def update_numero_convites_convocatoria(self):
        print(f"update_numero_convites_convocatoria")
        num = 0
        vars = ['convocatoria_presidente', 'convocatoria_vogal', 'convocatoria_arguente', 'convocatoria_aluno']

        for v in vars:
            print(f"{v} " + str(eval(f"self.{v}")))
            if eval(f"self.{v}"):
                num+=1
        self.write({'numero_convites_convocatoria': num})
        if num == 4:
            if self.estado == '070':
                self.update_estado()

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

    def convocatoria(self, resposta, juri):
        print(self.convite_arguente_url)
        print(self.convite_presidente_url)
        print(self.convite_vogal_url)
        print(f"CONVOCATORIA {juri} {resposta}")
        if resposta != '':
            if juri == 'cp' and resposta =='aceitado':
                self.write({'convocatoria_presidente': True})
            if juri == 'cv' and resposta =='aceitado':
                self.write({'convocatoria_vogal': True})
            if juri == 'ca' and resposta =='aceitado':
                self.write({'convocatoria_arguente': True})
            if juri == 'cal' and resposta =='aceitado':
                self.write({'convocatoria_aluno': True})
        self.update_numero_convites_convocatoria()
        self.update_estado()
        return self

    def link_presidente(self):
        if self.convite_presidente_url ==False:
            key = bytes(self.env['ir.config_parameter'].sudo().get_param('gest_diss.fernet_key',  'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='), 'utf-8')
            fernet = Fernet(key)
            now = datetime.now()
            link = f"p-/-{self._origin.id}-/-{self.juri_presidente_id.name}-/-{now}"
            print(link)
            token = (fernet.encrypt(link.encode())).decode()
            url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/invite/{token}"
            self.write({'convite_presidente_url' : url})

    def link_vogal(self):
        if self.convite_vogal_url == False:
            key =  bytes(self.env['ir.config_parameter'].sudo().get_param('gest_diss.fernet_key',  b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='), 'utf-8')
            fernet = Fernet(key)
            now = datetime.now()
            link = f"v-/-{self._origin.id}-/-{self.juri_vogal_id.name}-/-{now}"
            print(link)
            token = (fernet.encrypt(link.encode())).decode()
            url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/invite/{token}"
            self.write({'convite_vogal_url' : url})

    def link_arguente(self):

        if self.convite_arguente_url == False:
            key =  bytes(self.env['ir.config_parameter'].sudo().get_param('gest_diss.fernet_key',  b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='), 'utf-8')
            fernet = Fernet(key)
            now = datetime.now()
            link = f"a-/-{self.id}-/-{self.juri_arguente_id.name}-/-{now}"
            print(link)
            token = (fernet.encrypt(link.encode())).decode()
            url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/invite/{token}"
            self.write({'convite_arguente_url' : url})

    def gera_token_link(self, target=""):
        print(f"LINK {target} {type(self.id)} {type(models.NewId)}")

        if type(self.id) == models.NewId:
            oid = self.id.origin
        else:
            oid = self.id
        key = bytes(self.env['ir.config_parameter'].sudo().get_param('gest_diss.fernet_key',
                                                                     b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='),
                    'utf-8')
        fernet = Fernet(key)
        now = datetime.now()
        print(f"LINK {target} {type(self.id)} OID {oid}")
        link = f"{target}-/-{oid}-/-{self.name}-/-{now}"
        print(link)
        token = (fernet.encrypt(link.encode())).decode()

        return token

    def gera_link_vc(self):
        if self.link_vc_url == False:
            token = self.gera_token_link(target="linkvc")
            url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/linkvc/{token}"
            self.write({'link_vc_url': url})
            print(f"ENVIO PEDIDO LINK VC {self}")
            template_id = self.env.ref('gestao_dissertacoes.envio_pedido_link')
            self.message_post_with_template(template_id.id)

    def gera_link_anexos(self):
        print(f"GERA LINK ANEXOS {'=='*100} {self.anexos_url}")
        if self.anexos_url == False:
            token = self.gera_token_link(target="anexos")
            url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/anexos/{token}"
            #self.write({'link_vc_url': url})
            self.write({'anexos_url': url})


    def gera_link_nota(self):
        if self.nota_url == False:
            token = self.gera_token_link(target="nota")
            url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/nota/{token}"
            self.write({'nota_url': url})

    def gera_link_decl_arguente(self):
        print(f"GERA LINK DECL ARGUENTE {self.decl_arguente_url } {self.id}")
        if self.decl_arguente_url == False:
            token = self.gera_token_link(target="declArguente")
            url = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/declArguente/{token}"
            if type(self.id) == models.NewId:
                oid = self.id.origin
            else:
                oid = self.id
            #self.env['gest_diss.processo'].sudo().update(oid, {'decl_arguente_url': url})
            self.update({'decl_arguente_url': url})

    def update_link_vc(self, resposta):
        if resposta != '':
            self.write({'link_vc': resposta})
        return self

    def converter_data_hora_para_words(self, data_hora):
        print(f"converter_data_hora_para_words {data_hora}")
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        date_object = datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S").astimezone(local)

        ano = num2words(date_object.year, to='year', lang='pt_PT')
        mes = calendar.month_name[date_object.month]
        dia = num2words(date_object.day, to='year', lang='pt_PT')

        hora = num2words(date_object.hour, to='year', lang='pt_PT')
        minuto = num2words(date_object.minute, to='year', lang='pt_PT')

        data_words = dia + ' dias do mês de ' + mes.lower() + ' do ano de ' + ano
        if date_object.minute > 0:
            hora_words = hora + ' horas e ' + minuto + ' minutos'
        else:
            hora_words = hora + ' horas'

        return data_words, hora_words

    #def converter_data_para_words(self, data):
    #    print(f"converter_data_para_words {self} -- {data}")
    #    data_object = datetime.strptime(data, "%Y-%m-%d")
    #    ano = num2words(data_object.year, to='year', lang='pt_PT')
    #    mes = calendar.month_name[data_object.month]
    #    dia = num2words(data_object.day, to='year', lang='pt_PT')
    #    data_words = dia + ' de ' + mes.lower() + ' de ' + ano
    #    return data_words

    #def converter_data_para_str(self, data):
    #    date_object = datetime.strptime(data, "%Y-%m-%d")
    #    mes = calendar.month_name[date_object.month]
    #    data_str = str(date_object.day) + '.' + mes[:3] + '.' + str(date_object.year)
    #    return data_str

    @api.depends('enviar_decl_arguente', 'nota')
    def _change_enviar_decl_arguente(self):
        print(f"_ohange_enviar_decl_arguente {self.estado} {self.enviar_decl_arguente}")
        if self.estado >= '110' and self.enviar_decl_arguente == True:
            print(f"Enviar decl")
            self.enviar_pedido_assinatura_decl_arguente()
            print(f"Enviar decl2")

    def enviar_pedido_assinatura_decl_arguente(self):
        print(f"enviar_pedido_assinatura_decl_arguente {self.env.context} {self.id}")
        for objects in self:
            print(f"pedido {objects.enviar_decl_arguente} enviado {objects.decl_arguente_enviada}")
            if objects.decl_arguente_enviada == False and objects.enviar_decl_arguente ==True:
                id = None
                attach_name =''
                for obj in objects.attachment_ids:
                    #print(f"{obj.name}")
                    if obj.name == f"justificacao_arguente PDF":
                        id = obj.id
                        attach_name = f"justificacao_arguente.pdf"
                        break
                print(f"TESTE {id} {objects.decl_arguente_enviada} {objects} {objects.id} {dir(objects.id)}")
                if id == None:
                    print(f"DOC CREATINFG {objects.id} {objects._context.get('active_ids')}")
                    doc = objects.env['gest_diss.justificacao_arguente_doc'].create({
                        'tipo_ficheiro': 'pdf',
                        'processos_ids': [(4, objects.id)]
                    })
                    print("DOC CREATED")
                    res = doc.gerar_doc()
    
                    res = objects.env.ref('gestao_dissertacoes.gerar_justificacao_arguente_report_pdf').render_py3o(
                        res_ids=[objects.id, ], data=dict())
    
    
                    for obj in objects.attachment_ids:
                        #print(f"{obj.name}")
                        if obj.name == f"justificacao_arguente PDF":
                            id = obj.id
                            attach_name = f"justificacao_arguente.pdf"
                            break
                print(f"TESTE {id} {objects.decl_arguente_enviada} {objects} {objects.id} {dir(objects.id)}")
    
                if id != None:
                    print(f"Enviar pedido {objects.decl_arguente_url}")
                    if objects.decl_arguente_url == False:
                        objects.gera_link_decl_arguente()
                        print("LINK GERADO")
                        return
                    template_id = objects.env.ref('gestao_dissertacoes.pedido_assinatura')
                    template_id.attachment_ids = [(4, id)]
                    print(f"LINK: {objects.decl_arguente_url}")
                    objects.message_post_with_template(template_id.id)
                    template_id.attachment_ids = [(3, id)]
                    objects.update({'decl_arguente_enviada': True})
            else:
                msg = 'Erro: '
                if objects.decl_arguente_enviada:
                    msg =f"{msg} Pedido ja enviado, "
                if not objects.enviar_decl_arguente:
                    msg =f"{msg} Arguente nao pediu declaracao"
                #raise ValidationError(f"{msg}")

    def decl_arguente_assinada(self, data):
        print(f"decl_arguente_assinada")
        vals = {
            'res_model': 'gest_diss.processo',
            'res_id': self.id,
            'datas': base64.b64encode(data),
            'name': "declaracao_participacao.pdf",
            'mimetype': 'application/pdf',
        }

        if self.decl_arguente.id ==False:
            at_id1 = self.env['ir.attachment'].sudo().create(vals)
            self.write({'decl_arguente': at_id1})
            self.enviar_decl_arguente_assinada()

    def enviar_decl_arguente_assinada(self):
        print(f"enviar_decl_arguente_assinada")
        for rec in self:
            print(f"{rec} {rec.decl_arguente.id} {rec.decl_arguente_assinada_enviada}")
            if rec.decl_arguente.id == False or rec.decl_arguente_assinada_enviada == True:
                continue
            id = rec.decl_arguente.id

            if id :
                template_id = self.env.ref('gestao_dissertacoes.declaracao_arguente')
                template_id.attachment_ids = [(4, id)]
                self.message_post_with_template(template_id.id)
                template_id.attachment_ids = [(3, id)]
                self.write({'decl_arguente_assinada_enviada': True})

    def processa_notacontroller(self, atualizacao_diss:bool, nota:int):
        if atualizacao_diss:
            self.write({'atualizacao_diss': True})

        if self.nota ==0:
            self.write({'nota': nota})
            self.enviar_pedido_anexos()

    def processa_anexos_controller(self, kw):
        for key in ('anexo5a', 'anexo5b', 'dissertacao_final'):
            if kw.get(key, False):
                fname = kw.get(key, False).filename
                file = kw.get(key, False)
                data = file.read()

                vals = {
                    'res_model': 'gest_diss.processo',
                    'res_id': self.id,
                    'datas': base64.b64encode(data),
                    'name': fname,
                    'mimetype': 'application/pdf',
                }
                print(f"READ {key} {self.read([key])} {eval(f'self.{key}.id')}")
                if eval(f"self.{key}.id") == False:
                    # print(f"{vals}")
                    at_id1 = self.env['ir.attachment'].sudo().create(vals)
                    print(f"{at_id1}")
                    self.write({key: at_id1.id})

        print(f"DOC AVANCAR {self.dissertacao_final.id} {self.estado == '120' and (  self.anexo5a.id != False and self.anexo5b.id != False and (self.atualizacao_diss == False or self.dissertacao_final.id != False) )}")
        if self.estado == '120' and ( \
                        self.anexo5a.id != False and \
                        self.anexo5b.id != False and \
                        (self.atualizacao_diss == False or self.dissertacao_final.id != False) \
                ):
            self.avancar_action()