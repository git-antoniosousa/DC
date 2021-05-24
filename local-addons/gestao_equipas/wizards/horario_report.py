from datetime import timedelta, date
from odoo import models, fields, api


class HorarioReport(models.TransientModel):
    _name = 'horario.report'
    _description = 'Gerar horário'

    tipo = fields.Selection([('pessoal', 'Horário pessoal semanal'), ('mapa_treinos_jogos', 'Mapa de convocatórias')],
                            'Tipo',
                            default='pessoal',
                            required=True)
    horario_de = fields.Selection([('treinador', 'Treinador'), ('atleta', 'Atleta'), ('seccionista', 'Seccionista')],
                                  'Horário de', default='treinador')
    treinos_jogos_apresentar = fields.Selection([('todos', 'todos'), ('treinador', 'de um treinador'), ('escalao', 'de um escalão')],
                                                'Treinos e jogos a apresentar', default='todos')

    data_inicio = fields.Date('Data de início', required=True,
                              default=date.today() + timedelta(days=(7 - date.today().weekday())))
    data_fim = fields.Date('Data de fim', required=True,
                           default=(date.today() + timedelta(days=(7 - date.today().weekday()))) + timedelta(days=6))
    atleta = fields.Many2one('ges.atleta', 'Atleta')
    treinador = fields.Many2one('ges.treinador', 'Treinador')
    seccionista = fields.Many2one('ges.seccionista', 'Seccionista')
    escalao = fields.Many2one('ges.escalao', 'Escalão')

    @api.multi
    @api.onchange('data_inicio')
    def compute_datas(self):
        for r in self:
            data_inicio = fields.Date.from_string(r.data_inicio)
            # r.write({'data_fim': fields.Datetime.to_string(data_inicio + timedelta(days=6))})
            r.data_fim = fields.Date.to_string(data_inicio + timedelta(days=6))

    @api.multi
    @api.constrains('data_inicio', 'data_fim')
    def _check_dates(self):
        for r in self:
            start_date = fields.Date.from_string(r.data_inicio)
            end_date = fields.Date.from_string(r.data_fim)
            if r.tipo != 'pessoal':
                if end_date < start_date:
                    raise models.ValidationError('A data de fim não poderá ser '
                                                 'anterior à data de início')

    @api.multi
    def gen_horario_report(self):
        data = self.read(
            ['tipo', 'horario_de', 'data_inicio', 'data_fim', 'atleta', 'treinador', 'seccionista',
             'treinos_jogos_apresentar','escalao']
        )[0]

        if data['tipo'] == 'pessoal':
            data['data_fim'] = fields.Date.to_string(fields.Date.from_string(data['data_inicio']) + timedelta(days=6))
            if data['horario_de'] == 'atleta':
                treinos = self.env['ges.treino'].search(
                    [('atletas', 'in', data['atleta'][0]),
                     ('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                jogos = self.env['ges.jogo'].search(
                    [('atletas', 'in', data['atleta'][0]),
                     ('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                treinos_disponivel = []
                jogos_disponivel = []
                for treino in treinos:
                    convocatorias = list(filter(lambda line: line.atleta.id == data['atleta'][0],
                                                treino.evento_desportivo.convocatorias))
                    if len(convocatorias) > 0:
                        convocatoria = convocatorias[0]
                        if convocatoria.disponivel:
                            treinos_disponivel.append(treino.id)
                for jogo in jogos:
                    convocatorias = list(
                        filter(lambda line: line.atleta.id == data['atleta'][0], jogo.evento_desportivo.convocatorias))
                    if len(convocatorias) > 0:
                        convocatoria = convocatorias[0]
                        if convocatoria.disponivel:
                            jogos_disponivel.append(jogo.id)
                if len(treinos_disponivel) == 0 and len(jogos_disponivel) == 0:
                    raise models.ValidationError(
                        'Não existem treinos e jogos registados no período especificado.')
                data.update({'treinos_ids': treinos_disponivel, 'jogos_ids': jogos_disponivel})
                #data['atleta']=(data['atleta'][0],data['atleta'][0])
                return self.env.ref('gestao_equipas.report_atleta_horario_generate').report_action(self, data=data)
            elif data['horario_de'] == 'treinador':
                treinos = self.env['ges.treino'].search(
                    [('treinador', '=', data['treinador'][0]),
                     ('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                jogos = self.env['ges.jogo'].search(
                    [('treinador', '=', data['treinador'][0]),
                     ('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                if len(treinos.ids) == 0 and len(jogos.ids) == 0:
                    raise models.ValidationError(
                        'Não existem treinos e jogos registados no período especificado.')
                data.update({'treinos_ids': treinos.ids, 'jogos_ids': jogos.ids})
                return self.env.ref('gestao_equipas.report_treinador_horario_generate').report_action(self, data=data)
            elif data['horario_de'] == 'seccionista':
                treinos = self.env['ges.treino'].search(
                    [('seccionistas', 'in', data['seccionista'][0]),
                     ('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                jogos = self.env['ges.jogo'].search(
                    [('seccionistas', 'in', data['seccionista'][0]),
                     ('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                if len(treinos.ids) == 0 and len(jogos.ids) == 0:
                    raise models.ValidationError(
                        'Não existem treinos e jogos registados no período especificado.')
                data.update({'treinos_ids': treinos.ids, 'jogos_ids': jogos.ids})
                return self.env.ref('gestao_equipas.report_seccionista_horario_generate').report_action(self, data=data)
        elif data['tipo'] == 'mapa_treinos_jogos':
            if data['treinos_jogos_apresentar'] == 'todos':
                treinos = self.env['ges.treino'].search(
                    [('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                jogos = self.env['ges.jogo'].search(
                    [('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                if len(treinos.ids) == 0 and len(jogos.ids) == 0:
                    raise models.ValidationError(
                        'Não existem treinos e jogos registados no período especificado.')
                data.update({'treinos_ids': treinos.ids, 'jogos_ids': jogos.ids})
                return self.env.ref('gestao_equipas.report_mapa_generate').report_action(self, data=data)
            if data['treinos_jogos_apresentar'] == 'treinador':
                treinos = self.env['ges.treino'].search(
                    [('treinador', '=', data['treinador'][0]),
                     ('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                jogos = self.env['ges.jogo'].search(
                    [('treinador', '=', data['treinador'][0]),
                     ('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                if len(treinos.ids) == 0 and len(jogos.ids) == 0:
                    raise models.ValidationError(
                        'Não existem treinos e jogos registados no período especificado.')
                data.update({'treinos_ids': treinos.ids, 'jogos_ids': jogos.ids})
                return self.env.ref('gestao_equipas.report_mapa_generate').report_action(self, data=data)
            if data['treinos_jogos_apresentar'] == 'escalao':
                treinos = self.env['ges.treino'].search(
                    [('escalao', '=', data['escalao'][0]),
                     ('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                jogos = self.env['ges.jogo'].search(
                    [('escalao', '=', data['escalao'][0]),
                     ('start', '>=', data['data_inicio']),
                     ('stop', '<=', data['data_fim'])],
                    order='start DESC'
                )
                if len(treinos.ids) == 0 and len(jogos.ids) == 0:
                    raise models.ValidationError(
                        'Não existem treinos e jogos registados no período especificado.')
                data.update({'treinos_ids': treinos.ids, 'jogos_ids': jogos.ids})

                return self.env.ref('gestao_equipas.report_mapa_generate').report_action(self, data=data)
