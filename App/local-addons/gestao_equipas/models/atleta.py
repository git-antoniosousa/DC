# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta, date, datetime


class RegistoCargaFisica(models.Model):
    _name = 'ges.registo_carga_fisica'
    _description = 'Registo de carga física'
    _rec_name = ''

    n_treinos = fields.Integer('Número de treinos', readonly=True)
    n_jogos = fields.Integer('Número de jogos', readonly=True)

    n_horas_treino = fields.Float('Número de horas em treinos', readonly=True)
    n_horas_jogo = fields.Float('Número de horas em jogos', readonly=True)

    linhas_registo = fields.One2many('ges.linha_registo_carga_fisica', 'registo_carga_fisica', 'Linha de registo', readonly=True)

    @api.multi
    def name_get(self):
        repr = []
        for rec in self:
            repr.append((rec.id, "Registo do atleta"))
        return repr


class LinhaRegistoCargaFisica(models.Model):
    _name = 'ges.linha_registo_carga_fisica'
    _description = 'Linha de Registo de carga física'

    registo_carga_fisica = fields.Many2one('ges.registo_carga_fisica', 'Registo de carga física')
    categoria = fields.Many2one('ges.categoria_treino', 'Categoria de treino', readonly=True)
    n_minutos = fields.Integer('Número de minutos na categoria', readonly=True)


class Atleta(models.Model):
    _name = 'ges.atleta'
    _inherits = {'res.users': 'user_id', 'ges.registo_carga_fisica': 'registo_carga_fisica'}
    _description = 'Atleta'
    _order = 'name'
    _rec_name = 'name'

    user_id = fields.Many2one('res.users', ondelete='restrict', required=True)
    registo_carga_fisica = fields.Many2one('ges.registo_carga_fisica', 'Registo de carga física', ondelete="cascade",
                                           required=True)

    data_admissao = fields.Date('Data de admissão', required=True, default=fields.date.today())
    escalao = fields.Many2one('ges.escalao', string='Escalão')
    licencas_desportivas = fields.One2many('ges.licenca_desportiva', 'atleta_id', "Licenças Desportivas")
    validade_licenca_desportiva = fields.Date('Validade da licença desportiva',
                                              compute='get_validade_licenca',
                                              store=True)
    validade_exame_medico = fields.Date('Validade do Exame médico',
                                        readonly=True)
    dados_antropometricos = fields.One2many('ges.dados_antropometricos',
                                            'atleta_id',
                                            "Dados antropométricos")
    testes_fisicos = fields.One2many('ges.testes_fisicos',
                                            'atleta_id',
                                            "Testes Físicos")
    pais = fields.Many2many('ges.pai', string='Pais')
    equipas = fields.Many2many('ges.equipa', string='Equipas')
    treinos = fields.Many2many('ges.treino', string='Treinos')
    lesoes = fields.One2many(comodel_name='ges.lesao', inverse_name='atleta', string='Lesões')
    jogos = fields.Many2many('ges.jogo', string='Jogos')
    numerocamisola = fields.Integer(string = 'Número Camisola')
    posicao = fields.Selection(selection = [('GR', 'Guarda Redes'), ('CP','Jogador Campo')], default = 'CP', string = "Posição")

    @api.one
    def gen_fatura(self):
        self.user_id.partner_id.gen_fatura()

    @api.onchange('birthdate')
    def _compute_escalao(self):
        for r in self:
            if type(r.birthdate) != bool:
                e = r.escalao.calc_escalao(fields.Date.from_string(r.birthdate))
                if e is not None:
                    r.escalao = e
                else:
                    raise models.ValidationError(
                        'Não existe nenhum escalão que satisfaça a idade do atleta')

    @api.one
    def reg_exames_medicos(self):
        self.validade_exame_medico = self.prox_exame_medico(self.birthdate)

    def prox_exame_medico(self, data):
        next_year = date.today().year + 1
        data_nasc = fields.Date.from_string(data)
        data_nasc = data_nasc.replace(year=next_year)
        return  (data_nasc )

    @api.one
    @api.depends('licencas_desportivas.validade')
    def get_validade_licenca(self):
        if len(self.licencas_desportivas) == 0:
            return
        d = date.min
        for licenca in self.licencas_desportivas:
            dL = fields.Date.from_string(licenca.validade)
            if (dL > d):
                d = dL
        self.validade_licenca_desportiva = d

    @api.model
    def create(self, values):
        values['login'] = values['email']
        values['lang'] = 'pt_PT'
        values['tz'] = 'Europe/Lisbon'
        values['isSocio'] = True
        #values['escalao'] = self.escalao.calc_escalao(
        #    fields.Date.from_string(values['birthdate'])).id
        res = super(Atleta, self).create(values)
        atletas_group = self.env.ref('gestao_equipas.ges_user_atleta')
        atletas_group.write({
            'users': [(4, res.user_id.id)]
        })
        return res

    @api.multi
    def write(self, values):
        if 'email' in values:
            values['login'] = values['email']
        if 'birthdate' in values:
            values['escalao'] = self.escalao.calc_escalao(
                fields.Date.from_string(values['birthdate'])).id
        return super(Atleta, self).write(values)
