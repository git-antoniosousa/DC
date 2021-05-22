# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Equipa(models.Model):
    _name = 'ges.equipa'
    _description = 'Equipa'
    _order = 'name'

    name = fields.Char('Nome da equipa', required=True)
    escalao = fields.Many2one('ges.escalao', 'Escalão', required=True)
    epoca = fields.Many2one('ges.epoca', 'Época', required=True)
    atletas = fields.Many2many('ges.atleta', string='Atletas')

    @api.multi
    def name_get(self):
        repr = []
        for rec in self:
            datetime_inicio = fields.Date.from_string(rec.epoca.data_inicio)
            datetime_fim = fields.Date.from_string(rec.epoca.data_fim)
            ano_epoca = ' ({}/{})'.format(str(datetime_inicio.year)[-2:], str(datetime_fim.year)[-2:])
            repr.append((rec.id, str(rec.name) + ano_epoca))
        return repr

    @api.onchange('escalao')
    def mostra_atletas_escalao(self):
        for record in self:
            res = self.env['ges.atleta'].search([('escalao', '=', record.escalao.id)]).ids
            record.atletas = res
