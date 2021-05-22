import datetime
from datetime import timedelta, datetime, time, date
#import time
from odoo import models, api, fields
import pytz


class HorarioReport(models.AbstractModel):
    _name = 'report.gestao_equipas.report_horario_generate'

    def get_heading(self):
        return [(0, 'Segunda-feira'), (1, 'Terça-feira'), (2, 'Quarta-feira'), (3, 'Quinta-feira'), (4, 'Sexta-feira'),
                (5, 'Sábado'), (6, 'Domingo')]

    def get_eventos_of_day(self, eventos, dia):
        eventos_dia = list(filter(lambda evento: fields.Datetime.from_string(evento.start).weekday() == dia, eventos))
        return sorted(eventos_dia, key=lambda evento: fields.Datetime.from_string(evento.start))

    def get_treinos(self, treinos_ids):
        treinos = []
        for treino in self.env['ges.treino'].browse(treinos_ids):
            treinos.append(treino)
        return treinos

    def get_jogos(self, jogos_ids):
        jogos = []
        for jogo in self.env['ges.jogo'].browse(jogos_ids):
            jogos.append(jogo)
        return jogos

    def format_hour(self, data):
        tz_local = pytz.timezone(self.env.user.partner_id.tz or 'UTC')
        hour_naive = fields.Datetime.from_string(data)
        return (hour_naive + timedelta( seconds = tz_local.utcoffset(hour_naive).seconds)).strftime('%H:%M')

    def get_time(self, data):
        tz_local = pytz.timezone(self.env.user.partner_id.tz or 'UTC')

        data_inicio_naive = fields.Datetime.from_string(data)
        data_inicio = data_inicio_naive + timedelta(seconds = tz_local.utcoffset(data_inicio_naive).seconds)
        return time(hour=data_inicio.hour, minute=data_inicio.minute)

    def get_first_hour(self, eventos):
        tz_local = pytz.timezone(self.env.user.partner_id.tz or 'UTC')

        first_hour = time(hour=23, minute=59)
        for evento in eventos:
            data_inicio_naive = fields.Datetime.from_string(evento.start)
            td = timedelta(seconds = tz_local.utcoffset(data_inicio_naive).seconds)
            data_inicio = data_inicio_naive + td

            hour = time(hour=data_inicio.hour, minute=data_inicio.minute)
            if hour < first_hour:
                first_hour = hour
        return first_hour

    def get_position_height(self, evento, first_hour):
        factor = 1.1
        hour = self.get_time(evento.start)

        height = evento.duracao * factor

        if hour == first_hour:
            return 'top: 0px; left: 0px;', 'height: ' + str(height) + 'px;'
        else:
            difference = datetime.combine(date.min, hour) - datetime.combine(
                date.min, first_hour)
            top = (difference.seconds // 60) * factor
            return 'top: ' + str(top) + 'px; left: 0px;', 'height: ' + str(height) + 'px;'