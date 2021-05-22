# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class LinhaCategoriaTreino(models.Model):
    _name = 'ges.linha_categoria_treino'
    _description = 'Linha categoria de Treino'
    _order = 'categoria_treino'
    _rec_name = 'categoria_treino'

    categoria_treino = fields.Many2one('ges.categoria_treino',
                                       string='Categoria', ondelete='cascade', required=True)
    treino = fields.Many2one('ges.treino', string='Treino', ondelete='cascade')
    duracao = fields.Integer('Duração')


class Treino(models.Model):
    _name = 'ges.treino'
    _inherits = {'ges.evento_desportivo': 'evento_desportivo'}
    _description = 'Treino'

    evento_desportivo = fields.Many2one('ges.evento_desportivo', 'Evento desportivo', ondelete="cascade", required=True)
    sumario = fields.One2many('ges.linha_categoria_treino', 'treino',
                              string='Sumário')
    plano_treinos_jogos = fields.Many2one('ges.plano_treinos_jogos', 'Plano de treinos e jogos associado',
                                          ondelete="cascade")
    duracao_actual = fields.Float(string='Carga de exercícios', compute='sumario_duracao')

    @api.onchange('escalao')
    def mostra_atletas_escalao(self):
        for record in self:
            res = self.env['ges.atleta'].search([('escalao', '=', record.escalao.id)]).ids
            record.atletas = res

    def fechar_evento(self):
        for linha_presenca in self.evento_desportivo.presencas:
            if linha_presenca.presente:
                linhas_registo = []
                registo_carga_fisica = linha_presenca.atleta.registo_carga_fisica
                for linha_categoria in self.sumario:
                    if not (linha_categoria.categoria_treino.id in [x.categoria_treino.id for x in
                                                                    linha_presenca.exercicios_ausente]):
                        linhas_registo_filter = list(
                            filter(lambda linha: linha.categoria.id == linha_categoria.categoria_treino.id,
                                   registo_carga_fisica.linhas_registo))
                        if len(linhas_registo_filter) > 0:
                            linha_registo = linhas_registo_filter[0]
                            linha_registo.write({
                                'categoria': linha_categoria.categoria_treino.id,
                                'n_minutos': linha_registo['n_minutos'] + linha_categoria.duracao,
                            })
                        else:
                            valuesLinhaRegisto = {
                                'categoria': linha_categoria.categoria_treino.id,
                                'n_minutos': linha_categoria.duracao,
                            }
                            linhas_registo.append((0, 0, valuesLinhaRegisto))

                valuesRegisto = {
                    'n_treinos': registo_carga_fisica.n_treinos + 1,
                    'n_horas_treino': registo_carga_fisica.n_horas_treino + self.evento_desportivo.duracao / 60,
                    'linhas_registo': linhas_registo,
                }
                registo_carga_fisica.write(valuesRegisto)
        return self.evento_desportivo.fechar_evento()

    def marcar_presencas(self):
        return self.evento_desportivo.marcar_presencas()

    def marcar_presencas_from_list(self):
        for rec in self:
            if rec.evento_desportivo.state != 'aberto':
                raise models.ValidationError(
                    'As presenças só podem ser marcadas num treino em aberto.')
            rec.marcar_presencas()

    def fechar_evento_from_list(self):
        for rec in self:
            if rec.evento_desportivo.state != 'convocatorias_fechadas':
                raise models.ValidationError(
                    'O treino só pode ser fechado depois de marcadas as presenças.')
            rec.fechar_evento()

    def gen_registo_presencas(self):
        data = {
            'descricao': 'Treino',
            'evento_id': self.evento_desportivo.id,
        }
        return self.evento_desportivo.gen_registo_presencas(data)

    @api.onchange('convocatorias')
    def calc_values_convoc(self):
        for rec in self:
            rec.n_convocados = len(rec.atletas)
            rec.n_indisponiveis = len(list(filter(lambda l: not l.disponivel, rec.convocatorias)))

    @api.onchange('presencas')
    def calc_values_presencas(self):
        for rec in self:
            rec.n_faltas = len(list(filter(lambda l: not l.presente, rec.presencas)))
            rec.n_atrasos = len(list(filter(lambda l: l.atrasado and l.presente, rec.presencas)))
            rec.n_presentes = len(rec.presencas) - rec.n_faltas

    @api.onchange('start', 'stop')
    def compute_duracao(self):
        for r in self:
            if (type(r.start) != bool) and (type(r.stop) != bool):
                datetime_start = fields.Datetime.from_string(r.start)
                datetime_stop = fields.Datetime.from_string(r.stop)
                r.duracao = self.evento_desportivo.calc_duracao(datetime_start, datetime_stop)

    @api.onchange('sumario', 'duracao')
    def sumario_duracao(self):
        duracao_total = 0
        for linha in self.sumario:
            duracao_total += linha.duracao

        if duracao_total > self.duracao:
            raise models.ValidationError(
                'Duração dos exercícios do sumário ({} min) é superior à duração do treino ({} min)'.format(
                    duracao_total, self.duracao))
        else:
            if self.duracao == 0:
                self.duracao_actual = 0
            else:
                self.duracao_actual = (100 * duracao_total) / self.duracao

    def alterar_disponibilidade(self):
        atleta = self.env['ges.atleta'].search([('user_id', '=', self.env.user.id)])
        return self.evento_desportivo.alterar_disponibilidade(atleta)

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        default['state'] = 'aberto'
        return super(Treino, self).copy(default)

    @api.multi
    def name_get(self):
        repr = []
        for rec in self:
            if type(rec.local.descricao) == bool:
                local = ""
            else:
                local = " | " + rec.local.descricao
            novo_nome = 'Treino' + ' | ' + rec.escalao.designacao + local
            repr.append((rec.id, novo_nome))
        return repr

    @api.model
    def create(self, vals):
        vals['name'] = 'Treino'
        res = super(Treino, self).create(vals)
        res.write({
            'evento_ref': 'ges.treino,' + str(res.id),
        })
        return res

    @api.multi
    def unlink(self):
        for rec in self:
            rec.evento_desportivo.unlink()
        return super(Treino, self).unlink()
