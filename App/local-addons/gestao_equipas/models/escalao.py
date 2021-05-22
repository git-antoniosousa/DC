# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import *


class Escalao(models.Model):
    _name = 'ges.escalao'
    _description = 'Escalão'
    _order = 'idade_min'
    _rec_name = 'designacao'

    designacao = fields.Char('Designação', required=True)
    idade_min = fields.Integer('Idade mínima', required=True)
    idade_max = fields.Integer('Idade máxima', required=True)

    @api.constrains('idade_max')
    def _check_idades(self):
        for r in self:
            if r.idade_min >= r.idade_max:
                raise models.ValidationError(
                    'A idade máxima terá de ser maior do que a idade mínima.')

    def calc_escalao(self, data_nascimento):
        epocas = self.env['ges.epoca'].search([('atual', '=', 'True')])
        if len(epocas) > 0:
            data_inicio_epoca = fields.Date.from_string(epocas[0].data_inicio)
            data_fim_epoca = fields.Date.from_string(epocas[0].data_fim)
        else:
            raise models.ValidationError("O cálculo de escalão necessita de uma época atual definida.")

        if data_inicio_epoca.year == data_fim_epoca.year:
            fim_ano = date(data_inicio_epoca.year - 1, 12, 31)
        else:
            fim_ano = date(data_inicio_epoca.year, 12, 31)

        idade_fim_ano = relativedelta(fim_ano, data_nascimento).years

        e = self.search([('idade_min', '<=', idade_fim_ano), ('idade_max', '>=', idade_fim_ano)], limit=1)
        if len(e) > 0:
            return e
        return None
