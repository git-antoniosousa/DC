from odoo import api, models, fields
from datetime import datetime
import calendar
import locale
from num2words import num2words
import pytz
locale.setlocale(locale.LC_ALL, 'pt_PT')

class Defesa(models.Model):
    _name = "gest_diss.defesa"
    _description = 'Defesa de um aluno'
    _rec_name = 'data_hora'

    @api.depends("data_hora")
    def converter_hora_para_words(self):
        print(f" converter_hora_para_words {self}")
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        res = dict()
        for rec in self:
            #date_object = datetime.strptime(rec.data_hora, "%Y-%m-%d %H:%M:%S")

            date_object = rec.data_hora.astimezone(local)
            print(f"{rec.data_hora} ---> TZ {date_object}")
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
            res[rec.id] = hora_words
            rec.hora_words = hora_words
        print(f"Return {res}")
        return res
        #return data_words, hora_words

    @api.depends("data_hora")
    def converter_data_para_words(self):
        print(f" converter_data_para_words {self}")
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        res = dict()
        for rec in self:
            #data_object = datetime.strptime(rec.data_hora, "%Y-%m-%d")
            data_object = rec.data_hora.astimezone(local)
            ano = num2words(data_object.year, to='year', lang='pt_PT')
            mes = calendar.month_name[data_object.month]
            dia = num2words(data_object.day, to='year', lang='pt_PT')
            data_words = dia + ' de ' + mes.lower() + ' de ' + ano
            res[rec.id] = data_words
            rec.data_words = data_words
        print(f"Return {res}")
        return res

    @api.depends("data_hora")
    def converter_data_para_str(self):
        print(f" converter_data_para_str {self}")
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        res = dict()
        for rec in self:
            date_object = rec.data_hora.astimezone(local).strftime("%d.%b.%Y")
            res[rec.id] = date_object
            rec.data_str = date_object
        print(f"Return {res}")
        return res

    @api.depends("data_hora")
    def compute_data_defesa(self):
        user_tz = self.env.user.tz or str(pytz.utc)
        local = pytz.timezone(user_tz)
        res = dict()
        for rec in self:
            date_object = rec.data_hora.astimezone(local).strftime("%d-%m-%Y")
            res[rec.id] = date_object
            rec.data_defesa = date_object
        return res

    @api.depends("data_hora")
    def compute_hora_defesa(self):
        print(f" compute_hora_defesa {self}")
        res = dict()
        user_tz = self.env.user.tz or str(pytz.utc)
        local = pytz.timezone(user_tz)
        for rec in self:
            date_object = rec.data_hora.astimezone(local).strftime("%Hh%M")
            res[rec.id] = date_object
            rec.hora_defesa = date_object
        print(f"Return {res}")
        return res

    data_hora = fields.Datetime('Data e Hora')


    data_defesa = fields.Char(compute=compute_data_defesa, string="Data da Defesa")

    hora_defesa = fields.Char(compute=compute_hora_defesa, string="Hora da Defesa")

    data_words = fields.Char(compute=converter_data_para_words,  string="Data em Formato por Extenso")

    hora_words = fields.Char(compute=converter_hora_para_words, string="Hora em Formato por Extenso")

    # Exemplo: 12.Jun.2021
    data_str = fields.Char(compute=converter_data_para_str, string="Data em Formato Semi-Extenso")
    # Exemplo: 14h00
    hora_str = fields.Char(string="Hora em Formato por Semi-Extenso")

    local = fields.Selection([('presencial', 'Presencial'), ('virtual', 'Virtual')])
    sala = fields.Char(string="Sala")
    link_vc = fields.Char(string="Videoconferência")
    link_vc_url = fields.Char(string="link Videoconferência")

