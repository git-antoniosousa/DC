# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class TipoLesao(models.Model):
    _name = 'ges.tipo_lesao'
    _description = 'Tipo Lesão'
    _rec_name = 'descricao'

    descricao = fields.Char(string='Descrição', required=True)
    lesoes = fields.One2many(comodel_name='ges.lesao',
                             inverse_name='tipo_lesao', string='Lesões')


class Lesao(models.Model):
    _name = 'ges.lesao'
    _description = 'Lesão'

    atleta = fields.Many2one(comodel_name='ges.atleta', string='Atleta', required=True)
    create_date = fields.Date('Data de registo', readonly=True)

    data_ocorrencia = fields.Date('Data de ocorrência')
    ocorreu_num = fields.Selection([('treino', 'Treino'),
                                    ('jogo', 'Jogo'),
                                    ('outro', 'Outro')], 'Ocorreu num')
    treino = fields.Many2one('ges.treino', 'Treino', domain="[('start','<=',datetime.datetime.today())]")
    jogo = fields.Many2one('ges.jogo', 'Jogo', domain="[('start','<=',datetime.datetime.today())]")
    outro = fields.Char('Outro')
    observacoes_ocor = fields.Text('Observações')

    data_diagnostico = fields.Date('Data de diagnóstico')
    tipo_lesao = fields.Many2one('ges.tipo_lesao', 'Tipo de lesão')
    diagnostico = fields.Text('Diagnóstico')
    tempo_paragem = fields.Integer('Tempo de paragem (dias)')

    plano_tratamento = fields.Text('Plano de tratamento')
    responsaveis = fields.Many2many('res.partner', string='Responsáveis')
    data_conclusao = fields.Date('Data de conclusão')

    state = fields.Selection([('diagnostico', 'Em diagnóstico'),
                              ('tratamento', 'Em tratamento'),
                              ('tratada', 'Tratada')], default='diagnostico', string='Estado')

    def diagnosticar(self):
        self.write({
            'state': 'tratamento',
            'data_diagnostico': fields.Date.to_string(date.today())
        })

    def concluir(self):
        self.write({
            'state': 'tratada',
            'data_conclusao': fields.Date.to_string(date.today())
        })

    @api.onchange('ocorreu_num', 'treino', 'jogo')
    def get_data_ocorrencia(self):
        for r in self:
            if type(r.ocorreu_num) != bool:
                if r.ocorreu_num == 'treino':
                    if r.treino.id:
                        datetime_ocor = fields.Datetime.from_string(r.treino.start)
                        r.data_ocorrencia = fields.Date.to_string(datetime_ocor.date())
                elif r.ocorreu_num == 'jogo':
                    if r.jogo.id:
                        datetime_ocor = fields.Datetime.from_string(r.jogo.start)
                        r.data_ocorrencia = fields.Date.to_string(datetime_ocor.date())
