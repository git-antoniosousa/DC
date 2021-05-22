# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class EventoDesportivo(models.Model):
    _name = 'ges.evento_desportivo'
    _inherits = {'calendar.event': 'calendar_event'}
    _description = 'Evento desportivo'
    _order = 'start'

    state = fields.Selection([('aberto', 'Em aberto'),
                              ('convocatorias_fechadas', 'Convocatórias fechadas'),
                              ('fechado', 'Fechado')],
                             'Estado',
                             default='aberto')
    calendar_event = fields.Many2one('calendar.event', 'Evento de calendário', ondelete='cascade', required=True)
    duracao = fields.Integer(string='Duração (min)', readonly=True)
    local = fields.Many2one('ges.local', string='Local')
    treinador = fields.Many2many('ges.treinador', string='Treinador', required=True)

    seccionistas = fields.Many2many('ges.seccionista', string='Seccionistas')
    massagista = fields.Many2one('ges.massagista', string='Massagista', )
    escalao = fields.Many2one('ges.escalao', string='Escalão', required=True)
    atletas = fields.Many2many('ges.atleta', string='Atletas convocados')
    epoca = fields.Many2one('ges.epoca', string='Época')

    convocatorias = fields.One2many('ges.linha_convocatoria', 'evento', 'Convocatórias')
    presencas = fields.One2many('ges.linha_presenca', 'evento', 'Presenças')

    n_convocados = fields.Integer('N.º Convocados')
    n_indisponiveis = fields.Integer('N.º Indisponíveis', compute='_compute_indisponivel')
    n_faltas = fields.Integer('N.º Faltas', compute='_compute_faltas')
    n_atrasos = fields.Integer('N.º Atrasos', compute='_compute_atrasos')
    n_presentes = fields.Integer('N.º Presenças efetivas', compute='_compute_presentes')

    @api.depends('convocatorias')
    def _compute_indisponivel(self):
        for rec in self:
            res = 0
            for convocatoria in rec.convocatorias:
                if not convocatoria.disponivel:
                    res += 1
            rec.n_indisponiveis = res

    @api.depends('presencas')
    def _compute_faltas(self):
        for rec in self:
            res = 0
            for presenca in rec.presencas:
                if not presenca.presente:
                    res += 1
            rec.n_faltas = res

    @api.depends('presencas')
    def _compute_atrasos(self):
        for rec in self:
            res = 0
            for presenca in rec.presencas:
                if presenca.presente and presenca.atrasado:
                    res += 1
            rec.n_atrasos = res

    @api.depends('n_faltas')
    def _compute_presentes(self):
        for rec in self:
            rec.n_presentes = len(rec.presencas) - rec.n_faltas

    def alterar_disponibilidade(self, atleta):
        linhas = list(filter(lambda linha: linha.atleta.id == atleta.id, self.convocatorias))
        if len(linhas) > 0:
            linha = linhas[0]
            linha.write({
                'disponivel': not linha.disponivel
            })
        else:
            raise models.ValidationError('Não está convocado!')

    def marcar_presencas(self):
        linhas = []
        for linha_convocatoria in self.convocatorias:
            if linha_convocatoria.disponivel:
                linha = {
                    'atleta': linha_convocatoria.atleta.id,
                    'presente': True,
                    'atrasado': False
                }
                linhas.append((0, 0, linha))
        self.write({
            'presencas': linhas,
            'n_presentes': len(linhas),
            'state': 'convocatorias_fechadas'
        })

    def fechar_evento(self):
        self.write({
            'state': 'fechado',
        })

    def calc_duracao(self, start, stop):
        return (stop - start).seconds // 60

    @api.multi
    def gen_registo_presencas(self, data):
        data.update({
            'linhas_presenca': self.presencas,
        })
        return self.env.ref('gestao_equipas.report_reg_presencas_generate').report_action(self, data=data)

    @api.model
    def create(self, values):
        values['duracao'] = self.calc_duracao(
            fields.Datetime.from_string(values['start']), fields.Datetime.from_string(values['stop']))

        escalao = self.env['ges.escalao'].browse(values['escalao'])
        treinadores = self.env['ges.treinador'].browse(values['treinador'][0][2])

        values['description'] = 'Escalão: ' + escalao.designacao + ' Treinador: '
        treinadorname = ''

        local = self.env['ges.local'].browse(values['local'])
        values['location'] = local.descricao

        atletas = self.env['ges.atleta'].browse(values['atletas'][0][2])
        seccionistas = self.env['ges.seccionista'].browse(values['seccionistas'][0][2])
        partner_ids = []
        for atleta in atletas:
            partner_ids.append(atleta.user_id.partner_id.id)
        for seccionista in seccionistas:
            partner_ids.append(seccionista.user_id.partner_id.id)
        for treinador in treinadores:
            partner_ids.append(treinador.user_id.partner_id.id)
            treinadorname += treinador.user_id.name

        values['partner_ids'] = [[6, False, partner_ids]]
        values['description'] += treinadorname
        linhas = []
        for atleta in values['atletas'][0][2]:
            atletainfo = self.env['ges.atleta'].browse(atleta)
            linha = {
                'atleta': atleta,
                'disponivel': True,
                'numero': atletainfo.numerocamisola,
            }
            linhas.append((0, 0, linha))
        values['convocatorias'] = linhas

        values['n_convocados'] = len(values['atletas'][0][2])
        values['n_indisponiveis'] = 0

        return super(EventoDesportivo, self).create(values)

    @api.one
    def write(self, values):
        if ('start' in values) & ('stop' in values):
            values['duracao'] = self.calc_duracao(
                fields.Datetime.from_string(values['start']), fields.Datetime.from_string(values['stop']))
        else:
            if 'start' in values:
                values['duracao'] = self.calc_duracao(
                    fields.Datetime.from_string(values['start']), fields.Datetime.from_string(self.stop))
            else:
                if 'stop' in values:
                    values['duracao'] = self.calc_duracao(
                        fields.Datetime.from_string(self.start), fields.Datetime.from_string(values['stop']))

        partner_ids = []
        if 'atletas' in values:
            atletas_finais = self.env['ges.atleta'].browse(values['atletas'][0][2])

            atletas_antes = [linha.atleta.id for linha in self.convocatorias]

            atletas_eliminados = list(set(atletas_antes) - set(
                atletas_finais.ids))
            atletas_adicionados = list(set(atletas_finais.ids) - set(
                atletas_antes))

            values['n_convocados'] = self.n_convocados + len(atletas_adicionados) - len(atletas_eliminados)
            values['convocatorias'] = []

            for linha in self.convocatorias:
                if linha.atleta.id in atletas_eliminados:
                    values['convocatorias'].append((2, linha.id, False))

            for atleta in atletas_adicionados:
                linha = {
                    'atleta': atleta,
                    'disponivel': True,
                    'numero': self.env['ges.atleta'].browse(atleta).numerocamisola,
                }
                values['convocatorias'].append((0, 0, linha))
        else:
            atletas_finais = self.atletas

        for atleta in atletas_finais:
            partner_ids.append(atleta.user_id.partner_id.id)

        if 'escalao' in values:
            escalao = self.env['ges.escalao'].browse(values['escalao'])
        else:
            escalao = self.escalao

        if 'treinador' in values:
            treinadores = self.env['ges.treinador'].browse(values['treinador'][0][2])
        else:
            treinadores = self.treinador

        values['description'] = 'Escalão: ' + escalao.designacao + ' Treinador: '
        for treinador in treinadores:
            partner_ids.append(treinador.user_id.partner_id.id)
            values['description'] += treinador.name + ' '


        if 'local' in values:
            local = self.env['ges.local'].browse(values['local'])
        else:
            local = self.local
        values['location'] = local.descricao

        if 'seccionistas' in values:
            seccionistas = self.env['ges.seccionista'].browse(values['seccionistas'][0][2])
        else:
            seccionistas = self.seccionistas

        for seccionista in seccionistas:
            partner_ids.append(seccionista.user_id.partner_id.id)

        values['partner_ids'] = [[6, False, partner_ids]]

        return super(EventoDesportivo, self).write(values)

    @api.multi
    def unlink(self):
        for rec in self:
            rec.calendar_event.unlink();
        return super(EventoDesportivo, self).unlink()


class LinhaConvocatoria(models.Model):
    _name = 'ges.linha_convocatoria'
    _description = 'Linha convocatória'

    evento = fields.Many2one('ges.evento_desportivo', 'Evento desportivo')
    atleta = fields.Many2one('ges.atleta', string="Atleta", required=True, ondelete='cascade')
    disponivel = fields.Boolean('Disponivel?', default=True)
    numero = fields.Integer('Camisola')#, default = atleta.numerocamisola)

    @api.onchange('atleta')
    def _change_atleta(self):
        for rec in self:
            rec.numero = rec.atleta.numerocamisola
            
class LinhaPresenca(models.Model):
    _name = 'ges.linha_presenca'
    _description = 'Linha de presença'

    evento = fields.Many2one('ges.evento_desportivo', 'Evento desportivo')
    atleta = fields.Many2one('ges.atleta', string="Atleta", required=True, ondelete='cascade', readonly=True)
    presente = fields.Boolean('Presente?', default=False)
    atrasado = fields.Boolean('Atrasado?', default=False)

    exercicios_ausente = fields.Many2many('ges.linha_categoria_treino', string='Exercícios que não fez')

    @api.onchange('atrasado')
    def _constrain_atrasado(self):
        for rec in self:
            if rec.atrasado is True:
                rec.presente = True


class EventoCalendario(models.Model):
    _name = 'calendar.event'
    _inherit = 'calendar.event'

    evento_ref = fields.Reference([('ges.treino', 'Treino'), ('ges.jogo', 'Jogo')], 'Evento desportivo')
