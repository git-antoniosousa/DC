# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Competicao(models.Model):
    _name = 'ges.competicao'
    _description = 'Competição'
    _rec_name = 'designacao'

    designacao = fields.Char('Designação', required=True)

    epoca = fields.Many2one(comodel_name="ges.epoca", string="Época", required=True)

    @api.multi
    def name_get(self):
        repr = []
        for rec in self:
            datetime_inicio = fields.Date.from_string(rec.epoca.data_inicio)
            datetime_fim = fields.Date.from_string(rec.epoca.data_fim)
            ano_epoca = ' ({}/{})'.format(str(datetime_inicio.year)[-2:], str(datetime_fim.year)[-2:])
            repr.append((rec.id, str(rec.designacao) + ano_epoca))
        return repr
