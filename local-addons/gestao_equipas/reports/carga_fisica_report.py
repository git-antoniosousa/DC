# -*- coding: utf-8 -*-
from odoo import models, api, fields
import time
import pytz

class CargaFisicaReport(models.Model):

    _name = 'report.gestao_equipas.report_carga_fisica_evento_generate'

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

    def get_atleta(self, atleta_id):
        atleta = self.env['ges.atleta'].browse(atleta_id)
        return atleta

    def format_hour(self, data):
        tz_local = pytz.timezone(self.env.user.partner_id.tz or 'UTC')
        hour_naive = fields.Datetime.from_string(data)
        return (hour_naive + timedelta(seconds=tz_local.utcoffset(hour_naive).seconds)).strftime('%H:%M')

    @api.model
    def get_report_values(self, doc_ids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        atleta = self.get_atleta(data['atleta'][0])
        treinos = self.get_treinos(data['treinos_ids'])
        jogos = self.get_jogos(data['jogos_ids'])

        doc_args = {
            'doc_ids': doc_ids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            'time': time,
            'n_treinos': data['n_treinos'],
            'n_jogos': data['n_jogos'],
            'atleta': atleta,
            'format_hour': self.format_hour,
        }

        return doc_args