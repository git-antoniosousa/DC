# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
import math
import pytz

from odoo.exceptions import ValidationError


class PlanoTreinosJogos(models.Model):
    _name = 'ges.plano_treinos_jogos'
    _description = 'Plano de Treinos e Jogos'
    _order = 'name'

    name = fields.Char('Nome', required=True)
    data_inicio = fields.Date('Data de início', required=True, default=datetime.datetime.today())
    data_fim = fields.Date('Data de fim', required=True)
    epoca = fields.Many2one('ges.epoca', 'Época', required=True)
    linhas_plano_treinos_jogos = fields.One2many('ges.linha_plano_treinos_jogos', 'plano_treinos_jogos',
                                                 'Linhas de plano de treinos e jogos',
                                                 copy=True)
    linhas_plano_treinos_jogos_seg = fields.One2many('ges.linha_plano_treinos_jogos', 'plano_treinos_jogos',
                                                     'Linhas de plano de treinos e jogos',
                                                     domain=[('dia', '=', '0')])
    linhas_plano_treinos_jogos_ter = fields.One2many('ges.linha_plano_treinos_jogos', 'plano_treinos_jogos',
                                                     'Linhas de plano de treinos e jogos',
                                                     domain=[('dia', '=', '1')])
    linhas_plano_treinos_jogos_qua = fields.One2many('ges.linha_plano_treinos_jogos', 'plano_treinos_jogos',
                                                     'Linhas de plano de treinos e jogos',
                                                     domain=[('dia', '=', '2')])
    linhas_plano_treinos_jogos_qui = fields.One2many('ges.linha_plano_treinos_jogos', 'plano_treinos_jogos',
                                                     'Linhas de plano de treinos e jogos',
                                                     domain=[('dia', '=', '3')])
    linhas_plano_treinos_jogos_sex = fields.One2many('ges.linha_plano_treinos_jogos', 'plano_treinos_jogos',
                                                     'Linhas de plano de treinos e jogos',
                                                     domain=[('dia', '=', '4')])
    linhas_plano_treinos_jogos_sab = fields.One2many('ges.linha_plano_treinos_jogos', 'plano_treinos_jogos',
                                                     'Linhas de plano de treinos e jogos',
                                                     domain=[('dia', '=', '5')])
    linhas_plano_treinos_jogos_dom = fields.One2many('ges.linha_plano_treinos_jogos', 'plano_treinos_jogos',
                                                     'Linhas de plano de treinos e jogos',
                                                     domain=[('dia', '=', '6')])
    treinos = fields.One2many('ges.treino', 'plano_treinos_jogos', 'Treinos gerados')
    jogos = fields.One2many('ges.jogo', 'plano_treinos_jogos', 'Jogos gerados')
    canGen = fields.Boolean('Pode gerar treinos e jogos', default=True)

    @api.constrains('data_inicio', 'data_fim')
    def check_dates(self):
        start_date = fields.Date.from_string(self.data_inicio)
        end_date = fields.Date.from_string(self.data_fim)
        if start_date > end_date:
            raise ValidationError("A data de fim não pode ser anterior à data de ínicio.")
        if start_date < datetime.date.today():
            raise ValidationError("A data de início não poderá ser uma data passada.")
        if start_date == end_date:
            raise ValidationError("A data de início e de fim devem ser diferentes")

    @api.onchange('data_inicio')
    def _change_data_inicio(self):
        for rec in self:
            rec.data_fim = rec.data_inicio

    def floatToTime(self, float):
        factor = float < 0 and -1 or 1
        val = abs(float)
        hour = factor * int(math.floor(val))
        min = int(round((val % 1) * 60))
        return datetime.time(hour=hour, minute=min, second=0)

    @api.one
    def gen_treinos(self):
        treinos = []
        jogos = []
        start_date = fields.Date.from_string(self.data_inicio)
        end_date = fields.Date.from_string(self.data_fim)
        for dia in range((end_date - start_date).days + 1):
            current_date = start_date + datetime.timedelta(days=dia)
            for line in self.linhas_plano_treinos_jogos:
                if int(line.dia) == current_date.weekday():
                    hour_inicio = self.floatToTime(line.hora_inicio)
                    hour_fim = self.floatToTime(line.hora_fim)

                    datetime_inicio = datetime.datetime(current_date.year, current_date.month, current_date.day,
                                                        hour_inicio.hour, hour_inicio.minute, hour_inicio.second)
                    datetime_fim = datetime.datetime(current_date.year, current_date.month, current_date.day,
                                                     hour_fim.hour, hour_fim.minute, hour_fim.second)

                    if datetime_inicio < datetime.datetime.today():
                        continue

                    atletasConvocados_ids = list()
                    for equipa in line.equipas:
                        atletasConvocados_ids.extend(equipa.atletas.ids)
                    atletasConvocados = [[6, False, atletasConvocados_ids]]

                    seccionistas = [[6, False, line.seccionistas.ids]]

                    treinador = [(6, False, line.treinador.ids)]

                    tz_local = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
                    duracao = (datetime_fim - datetime_inicio).seconds // 60

                    if line.tipo == 'treino':
                        sumario = list()
                        for linha_categoria_treino in line.linhas_categoria_treino:
                            valuesLinha = {
                                'categoria_treino': linha_categoria_treino.categoria_treino.id,
                                'duracao': linha_categoria_treino.duracao,
                            }
                            sumario.append((0, 0, valuesLinha))

                        valuesTreino = {
                            'start': fields.Datetime.to_string(
                                tz_local.localize(datetime_inicio, is_dst=None).astimezone(pytz.utc)),
                            'stop': fields.Datetime.to_string(
                                tz_local.localize(datetime_fim, is_dst=None).astimezone(pytz.utc)),
                            'duracao': duracao,
                            'local': line.local.id,
                            'treinador': treinador,
                            'seccionistas': seccionistas,
                            'escalao': line.escalao.id,
                            'atletas': atletasConvocados,
                            'epoca': self.epoca.id,
                            'sumario': sumario
                        }
                        treino = self.env['ges.treino'].create(valuesTreino)
                        treinos.append((4, treino.id, 0))
                    else:
                        valuesJogo = {
                            'start': fields.Datetime.to_string(
                                tz_local.localize(datetime_inicio, is_dst=None).astimezone(pytz.utc)),
                            'stop': fields.Datetime.to_string(
                                tz_local.localize(datetime_fim, is_dst=None).astimezone(pytz.utc)),
                            'duracao': duracao,
                            'local': line.local.id,
                            'treinador': treinador,
                            'seccionistas': seccionistas,
                            'escalao': line.escalao.id,
                            'epoca': self.epoca.id,
                            'atletas': atletasConvocados,
                        }
                        jogo = self.env['ges.jogo'].create(valuesJogo)
                        jogos.append((4, jogo.id, 0))

        self.treinos = treinos
        self.jogos = jogos
        self.canGen = False

    @api.one
    def unlink_treinos_jogos(self):
        for treino in self.treinos:
            if fields.Datetime.from_string(treino.start) >= datetime.datetime.today():
                treino.unlink()
        for jogo in self.jogos:
            if fields.Datetime.from_string(jogo.start) >= datetime.datetime.today():
                jogo.unlink()
        self.canGen = True

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        default['treinos'] = False
        default['canGen'] = True

        date_inicio = fields.Datetime.from_string(self.data_inicio)
        date_fim = fields.Datetime.from_string(self.data_fim)

        td = date_fim - date_inicio

        prox_inicio = date_fim + datetime.timedelta(days=1)
        prox_fim = prox_inicio + td

        default['data_inicio'] = fields.Datetime.to_string(prox_inicio)
        default['data_fim'] = fields.Datetime.to_string(prox_fim)

        copied_count = self.search_count(
            [('name', '=like', u"Cópia de {}%".format(self.name))])
        if not copied_count:
            new_name = u"Cópia de {}".format(self.name)
        else:
            new_name = u"Cópia de {} ({})".format(self.name, copied_count)
        default['name'] = new_name

        return super(PlanoTreinosJogos, self).copy(default)


class LinhaPlanoTreinosJogos(models.Model):
    _name = 'ges.linha_plano_treinos_jogos'
    _description = 'Linha de plano de treinos e jogos'

    plano_treinos_jogos = fields.Many2one('ges.plano_treinos_jogos', 'Plano de treinos e jogos')
    dia = fields.Selection([('0', 'Segunda'),
                            ('1', 'Terça'),
                            ('2', 'Quarta'),
                            ('3', 'Quinta'),
                            ('4', 'Sexta'),
                            ('5', 'Sábado'),
                            ('6', 'Domingo')], required=True)
    hora_inicio = fields.Float('Início', required=True)
    hora_fim = fields.Float('Fim', required=True)
    treinador = fields.Many2many('ges.treinador', string='Treinadores', required=True)
    linhas_categoria_treino = fields.One2many('ges.linha_categoria_treino_planeamento', 'planeamento', 'Sumário')
    local = fields.Many2one('ges.local', 'Local', required=True)
    escalao = fields.Many2one('ges.escalao', 'Escalão', required=True)
    equipas = fields.Many2many('ges.equipa', string='Equipas', required=True)
    seccionistas = fields.Many2many('ges.seccionista', string='Seccionistas')
    tipo = fields.Selection([('treino', 'Treino'), ('jogo', 'Jogo')], 'Tipo', default='treino')

    @api.constrains('hora_fim')
    @api.onchange('hora_fim', 'hora_inicio')
    def _check_hora_fim(self):
        for rec in self:
            if rec.hora_fim * rec.hora_inicio != 0:
                if rec.hora_fim < rec.hora_inicio:
                    raise models.ValidationError('A hora de fim tem que ser posterior à hora de início.')

    @api.onchange('hora_inicio')
    def _change_hora_fim(self):
        for rec in self:
            if rec.hora_fim != 0:
                rec.hora_fim = rec.hora_inicio

    @api.onchange('linhas_categoria_treino', 'hora_inicio', 'hora_fim')
    def sumario_duracao(self):
        hour_inicio = self.plano_treinos_jogos.floatToTime(self.hora_inicio)
        hour_fim = self.plano_treinos_jogos.floatToTime(self.hora_fim)

        duracao_evento = datetime.datetime.combine(datetime.date.min, hour_fim) - datetime.datetime.combine(
            datetime.date.min, hour_inicio)
        duracao_evento = duracao_evento.seconds // 60

        duracao_total = 0
        for linha in self.linhas_categoria_treino:
            duracao_total += linha.duracao

        if duracao_total > duracao_evento:
            raise models.ValidationError(
                'Duração dos exercícios do sumário ({} min) é superior à duração do treino ({} min)'.format(
                    duracao_total, duracao_evento))


class LinhaCategoriaTreinoPlaneamento(models.Model):
    _name = 'ges.linha_categoria_treino_planeamento'
    _description = 'Linha de categoria de treino - planeamento'

    categoria_treino = fields.Many2one('ges.categoria_treino', string='Categoria', ondelete='cascade', required=True)
    planeamento = fields.Many2one('ges.plano_treinos_jogos', string='Planeamento', ondelete='cascade')
    duracao = fields.Integer('Duração')

    @api.multi
    def name_get(self):
        repr = []
        for rec in self:
            repr.append((rec.id, str(rec.categoria_treino.display_name) + ", " + str(rec.duracao) + " min"))
        return repr
