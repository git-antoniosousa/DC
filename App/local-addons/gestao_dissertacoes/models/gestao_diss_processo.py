import calendar, time
import locale
from num2words import num2words
from datetime import datetime
from odoo import api, models, fields

# Definir o locale PT
locale.setlocale(locale.LC_ALL, 'pt_PT')

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
    data_homologacao_words = fields.Char(string="Data de Homologação por Extenso")

    # --- data primeira reuniao ---
    data_hora_primeira_reuniao = fields.Datetime(string="Data e Hora da Primeira Reunião")
    data_primeira_reuniao_words = fields.Char(string="Data da Primeira Reunião por Extenso")
    hora_primeira_reuniao_words = fields.Char(string="Data da Primeira Reunião por Extenso")

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
        if self.nome and self.numero and self.curso and self.email \
                and self.diss_titulo and self.orientador_id and self.coorientador_id:
            return self.write({'estado': 'correcoes'})

    def correcoes_action(self):
        return self.write({'estado': 'proposta_juri'})

    def prop_juri_action(self):
        if self.juri_presidente_id and self.juri_vogal_id and self.juri_vogal_id \
                and self.data_hora and self.local and self.sala:
            return self.write({'estado': 'aguardar_confirmacao_juri'})

    def juri_confirmado_action(self):
        return self.write({'estado': 'aguardar_homologacao'})

    def aguardar_homologacao_action(self):
        return self.write({'estado': 'homologacao'})

    def homologacao_action(self):
        if self.data_homologacao:
            return self.write({'estado': 'ata_primeira_reuniao'})

    def ata_primeira_reuniao_action(self):
        return self.write({'estado': 'declaracao_aluno'})

    def declaracao_aluno_action(self):
        return self.write({'estado': 'ata_prova'})

    def ata_prova_action(self):
        return self.write({'estado': 'registo_nota'})

    def registo_nota_action(self):
        if self.nota:
            return self.write({'estado': 'aguardar_versao_final'})

    def aguardar_versao_final_action(self):
        return self.write({'estado': 'finalizado'})

    def finalizar_action(self):
        pass

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

    def convite(self, resposta, juri):
        if resposta != '':
            if juri == 'p':
                return self.write({'convite_presidente': resposta})
            if juri == 'v':
                return self.write({'convite_vogal': resposta})
            if juri == 'a':
                return self.write({'convite_arguente': resposta})
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