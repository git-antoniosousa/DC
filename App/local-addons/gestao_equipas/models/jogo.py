# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json


class EventoJogo(models.AbstractModel):
    _name = 'ges.evento_jogo'
    _description = 'Evento Jogo'
    _order = 'minuto'

    jogo = fields.Many2one(comodel_name='ges.jogo',
                           string='Jogo')

    def get_parts(self):
        #return [('1', '1ª Parte'), ('2', '2ª Parte'), ('3', '3ª Parte'), ('4', '4ª Parte')]
        res = list()
        print("+* GET PARTS **", self, "GAME ", self.jogo, "ID ", self.id,  " CTX ", self.env.context)
        if self.id == False or self.jogo == False:
            if 'default_jogo' in self.env.context.keys():
                jogo = self.env['ges.jogo'].browse( self.env.context['default_jogo'] )
                for i in range(1, int(jogo.numero_partes) + 1):
                    res.append((str(i), str(i) + "ª Parte"))
            else:
                return [('1', '1ª Parte'), ('2', '2ª Parte')]

        else:
            print("+* GET PARTS **", self, self.jogo , self.id, self.env.context)
            for record in self:
                print ("GET PARTS", record.jogo, type(record.jogo.numero_partes), (record.jogo.numero_partes))
                for i in range(1, int(record.jogo.numero_partes)+1 ):
                    res.append(str(i), str(i)+"ª Parte")
                print(res)
        for i in res:
            #print(i[0].encode('ascii', 'ignore'), i[1].encode('ascii', 'ignore'))
            print(i[0], i[1])
        print(res)
        return res

    #parte = fields.Selection([('1', '1ª Parte'), ('2', '2ª Parte'), ('3', '3ª Parte'), ('4', '4ª Parte')],
    #                         string='Parte', default='1',
    #                         readonly=True, store=True)

    parte = fields.Selection( selection = get_parts,
                             string='Parte',# default='0',
                             store=True)

    minuto = fields.Float(string='Minuto', required=True)

    a_favor = fields.Selection([('f', 'A favor'), ('c', 'Contra')],
                               required=True,
                               string="A favor?",
                               default='f')

    atleta = fields.Many2one(comodel_name='ges.atleta',
                             string='Atleta')

    #def get_parte(self, minuto, jogo):
    #    if minuto < jogo.duracao_parte.tempo_parte:
    #        return '1'
    #    else:
    #        return '2'

    #@api.onchange('minuto')
    #def gen_parte(self):
    #    for record in self:
    #        record.parte = self.get_parte(record.minuto, record.jogo)

    #@api.model
    #def write(self, vals):
    #    if 'minuto' in vals:
    #        vals['parte'] = self.get_parte(vals['minuto'], self.jogo)
    #    return super(EventoJogo, self).write(vals)

    @api.model
    def create(self, vals):
        print("Create ", vals)
        jogo = self.env['ges.jogo'].browse(vals['jogo'])
        #vals['parte'] = self.get_parte(vals['minuto'], jogo)
        return super(EventoJogo, self).create(vals)


class Substituicao(models.Model):
    _name = 'ges.jogo_substituicao'
    _inherit = ['ges.evento_jogo']
    _description = 'Substituição'

    atleta_entrou = fields.Many2one(comodel_name="ges.atleta",
                                    string="Entrou", required=True)

    atleta_saiu = fields.Many2one(comodel_name="ges.atleta",
                                  string="Saiu", required=True)


class Falta(models.Model):
    _name = 'ges.jogo_falta'
    _inherit = ['ges.evento_jogo']
    _description = 'Falta'

    zona = fields.Many2one(comodel_name='ges.zona', string='Zona')


class Accao(models.Model):
    _name = 'ges.jogo_accao'
    _inherit = ['ges.evento_jogo']
    _description = 'Acção'

    tipo = fields.Selection([('ao', 'Ataque organizado'),
                             ('ar', 'Ataque rápido'),
                             ('ca', 'Contra-ataque'),
                             ('p', 'Penalti'),
                             ('ld', 'Livre Directo'),
                             ('li', 'Livre Indirecto'),
                             ('pwp', 'PWP')])

    zona = fields.Many2one(comodel_name='ges.zona', string='Zona')


class AccaoOfensiva(models.Model):
    _name = 'ges.jogo_accao_ofensiva'
    _inherit = ['ges.evento_jogo']
    _description = 'Acção Ofensiva'

    resultado = fields.Selection([('d', 'Desarme'),
                                  ('r', 'Recuperação'),
                                  ('i', 'Intercepção'),
                                  ('e', 'Erro próprio')])

    zona = fields.Many2one(comodel_name='ges.zona', string='Zona')


class Remate(models.Model):
    _name = 'ges.jogo_remate'
    _inherit = ['ges.evento_jogo']
    _description = 'Remate'

    zona = fields.Many2one(comodel_name='ges.zona', string='Zona')
    resultado = fields.Selection([('d', 'Defesa GR'),
                                  ('f', 'Fora'),
                                  ('i', 'Interceptado'),
                                  ('g', 'Golo')])


class Golo(models.Model):
    _name = 'ges.jogo_golo'
    _inherit = ['ges.evento_jogo']
    _description = 'Golo'


class Suspensao(models.Model):
    _name = 'ges.jogo_suspensao'
    _inherit = ['ges.evento_jogo']
    _description = 'Suspensão'

    tipo = fields.Selection([('1', '1ª'), ('2', '2ª'), ('3', '3ª')],
                            string='Nº Suspensão',
                            required=True)


class Cartao(models.Model):
    _name = 'ges.jogo_cartao'
    _inherit = ['ges.evento_jogo']
    _description = 'Mostragem de cartão'

    tipo = fields.Selection([('a', 'Azul'), ('v', 'Vermelho')],
                            string='Tipo Cartão',
                            required=True)


class Jogo(models.Model):
    _name = 'ges.jogo'
    _inherits = {'ges.evento_desportivo': 'evento_desportivo'}
    _description = 'Jogo'

    treinador_principal = fields.Many2one('ges.treinador', string="Treinador Principal",

                                         )

    evento_desportivo = fields.Many2one('ges.evento_desportivo',
                                        'Evento desportivo', ondelete='cascade',
                                        required=True)

    plano_treinos_jogos = fields.Many2one('ges.plano_treinos_jogos',
                                          'Plano de treinos e jogos associado',
                                          ondelete="cascade")

    competicao = fields.Many2one(comodel_name='ges.competicao',
                                 string='Competição')

    numero = fields.Char('Número de jogo')

    em_casa = fields.Selection([('s', 'Sim'),
                                ('n', 'Não')],
                               string='Em casa',
                               default='s')

    equipa_adversaria = fields.Many2one(comodel_name='ges.equipa_adversaria',
                                        string='Equipa Adversária')

    usar_estatisticas = fields.Boolean('Registar estatísticas', default=False)

    alinhamento_inicial = fields.Many2many(comodel_name="ges.atleta", relation='alinhamento_inicial')

    duracao_parte = fields.Many2one(comodel_name="ges.tempo_parte",
                                    string="Tempo de cada parte (min)",
                                    required=False)
    numero_partes = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')],
                             string='Número de Partes', default='2',
                             )

    cartoes = fields.One2many(comodel_name='ges.jogo_cartao',
                              inverse_name='jogo',
                              string='Cartões',
                              ondelete='cascade')

    suspensoes = fields.One2many(comodel_name='ges.jogo_suspensao',
                                 inverse_name='jogo',
                                 string='Suspensões',
                                 ondelete='cascade')

    golos = fields.One2many(comodel_name='ges.jogo_golo',
                            inverse_name='jogo',
                            string='Golos',
                            ondelete='cascade')

    remates = fields.One2many(comodel_name='ges.jogo_remate',
                              inverse_name='jogo',
                              string='Remates',
                              ondelete='cascade')

    accoes_ofensivas = fields.One2many(comodel_name='ges.jogo_accao_ofensiva',
                                       inverse_name='jogo',
                                       string='Acções ofensivas',
                                       ondelete='cascade')

    accoes = fields.One2many(comodel_name='ges.jogo_accao',
                             inverse_name='jogo',
                             string='Acções',
                             ondelete='cascade')

    faltas = fields.One2many(comodel_name='ges.jogo_falta',
                             inverse_name='jogo',
                             string='Faltas',
                             ondelete='cascade')

    substituicoes = fields.One2many(comodel_name='ges.jogo_substituicao',
                                    inverse_name='jogo',
                                    string="Substituições",
                                    ondelete='cascade')
    antecedencia = fields.Float(string="Antecedência Apresentação (h)", digits=(1,1), default=1.5)

    atletas_dentro = fields.Many2many('ges.atleta', string='Atletas a jogar', relation='atletas_dentro')
    atletas_fora = fields.Many2many('ges.atleta', string='Atletas fora do jogo', relation='atletas_fora')

    @api.onchange('escalao')
    def gen_atletas_escalao(self):
        for record in self:
            res = self.env['ges.atleta'].search([('escalao', '=', record.escalao.id)]).ids
            record.atletas = res

    @api.onchange('atletas', 'presencas')
    def gen_alinhamento_inicial(self):
        for record in self:
            if record.state == 'aberto':
                record.alinhamento_inicial = record.atletas.ids
            else:
                atletas = []
                for linha_presenca in record.presencas:
                    if linha_presenca.presente:
                        atletas.append(linha_presenca.atleta.id)
                record.alinhamento_inicial = atletas

    @api.onchange('alinhamento_inicial')
    def gen_atletas_dentro(self):
        for record in self:
            if record.state == 'aberto':
                atletas_presentes = record.atletas.ids
            else:
                atletas_presentes = []
                for linha_presenca in record.presencas:
                    if linha_presenca.presente:
                        atletas_presentes.append(linha_presenca.atleta.id)
            record.atletas_dentro = record.alinhamento_inicial.ids
            record.atletas_fora = list(set(atletas_presentes) - set(record.alinhamento_inicial.ids))

    def calc_estado_atleta(self, atleta, alinhamento_inicial, substituicoes):
        estado = 'f'
        if atleta.id in alinhamento_inicial.ids:
            estado = 'd'
        for substituicao in substituicoes:
            if substituicao.atleta_entrou.id == atleta.id:
                estado = 'd'
            elif substituicao.atleta_saiu.id == atleta.id:
                estado = 'f'
        return estado

    @api.onchange('substituicoes')
    def gen_atletas_dentro_e_fora(self):
        for record in self:
            atletas_dentro = []
            atletas_fora = []
            for linha_presenca in record.presencas:
                estado = self.calc_estado_atleta(linha_presenca.atleta, record.alinhamento_inicial,
                                                 record.substituicoes)
                if linha_presenca.presente:
                    if estado == 'd':
                        atletas_dentro.append(linha_presenca.atleta.id)
                    else:
                        atletas_fora.append(linha_presenca.atleta.id)
            record.atletas_dentro = atletas_dentro
            record.atletas_fora = atletas_fora

    @api.onchange('start', 'stop')
    def compute_duracao(self):
        for r in self:
            if (type(r.start) != bool) and (type(r.stop) != bool):
                datetime_start = fields.Datetime.from_string(r.start)
                datetime_stop = fields.Datetime.from_string(r.stop)
                r.duracao = self.evento_desportivo.calc_duracao(datetime_start,
                                                                datetime_stop)

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

    def marcar_presencas(self):
        return self.evento_desportivo.marcar_presencas()

    def calc_timeline(self, atleta):
        timeline = []
        if atleta.id in self.alinhamento_inicial.ids:
            timeline.append((0, 'e'))
        for substituicao in self.substituicoes:
            if substituicao.atleta_entrou.id == atleta.id:
                timeline.append((substituicao.minuto, 'e'))
            elif substituicao.atleta_saiu.id == atleta.id:
                timeline.append((substituicao.minuto, 's'))
        if len(timeline) > 0:
            if timeline[-1][1] == 'e':
                timeline.append((self.duracao_parte.tempo_parte * 2, 's'))
        return timeline

    def calc_tempo_jogo(self, atleta):
        timeline = self.calc_timeline(atleta)
        print("\n\n" + str(timeline))
        tempo_jogo = 0
        for pos in range(0, len(timeline), 2):
            tempo_jogo += timeline[pos + 1][0] - timeline[pos][0]
        return tempo_jogo

    def fechar_evento(self):
        for linha_presenca in self.evento_desportivo.presencas:
            if not self.usar_estatisticas:
                tempo_jogo = self.evento_desportivo.duracao
            else:
                tempo_jogo = self.calc_tempo_jogo(linha_presenca.atleta)
            registo_carga_fisica = linha_presenca.atleta.registo_carga_fisica
            valuesRegisto = {
                'n_jogos': registo_carga_fisica.n_jogos + 1,
                'n_horas_jogo': registo_carga_fisica.n_horas_jogo + tempo_jogo / 60,
            }
            registo_carga_fisica.write(valuesRegisto)
        return self.evento_desportivo.fechar_evento()

    def marcar_presencas_from_list(self):
        for rec in self:
            if rec.evento_desportivo.state != 'aberto':
                raise models.ValidationError(
                    'As presenças só podem ser marcadas num jogo em aberto.')
            rec.marcar_presencas()

    def fechar_evento_from_list(self):
        for rec in self:
            if rec.evento_desportivo.state != 'convocatorias_fechadas':
                raise models.ValidationError(
                    'O jogo só pode ser fechado depois de marcadas as presenças.')
            rec.fechar_evento()

    def gen_registo_presencas(self):
        data = {
            'descricao': 'Jogo',
            'evento_id': self.evento_desportivo.id,
        }
        return self.evento_desportivo.gen_registo_presencas(data)

    def alterar_disponibilidade(self):
        atleta = self.env['ges.atleta'].search([('user_id', '=', self.env.user.id)])
        return self.evento_desportivo.alterar_disponibilidade(atleta)

    @api.multi
    def gen_folha_convocatorias(self):
        data = {
            'jogo_id': self.id,
        }
        return self.env.ref(
            'gestao_equipas.report_folha_convoc_generate').report_action(self, data=data)


    def get_numcamisola(self, atleta):

        for lc in self.convocatorias:
            if lc.atleta == atleta:
                return lc.numero


    def enviar_convocatoria(self):
        self.ensure_one()
        jogo = self.gen_folha_convocatorias()
        #ctx = self.env.context
        #ctx['active_model'] = 'horario.report'
        #ctx['active_id'] = j
        data = {
            'jogo_id': self.id,
        }

        print("INFOOOO",str(jogo))
        pdf2 =  self.env.ref(
            'gestao_equipas.report_folha_convoc_generate').render(self.id, data=data)
        pdf2 = self.env['gestao_equipas.report_folha_convoc_evento_generate'].download(None, jogo['data'])
        #pdf2 = self.report.download('gestao_equipas.report_folha_convoc_evento_generate', None, jogo['data'])
        fname = "jogo" + str(j) + ".pdf"
        lfiles.append(fname)
        f = open(fname, 'wb')
        f.write(pdf2.read())
        f.close()
        pass

    @api.multi
    def gen_folha_convocatorias_fpp(self):
        info=self.read()
        #print(info)
        print(json.dumps(info))

        dados ={
            'Compet': '',
            'JogoNum': '',
            'Equipa': '',
            'Data': '',
            'Num2': '',
            'Num4': '',
            'Num3': '',
            'Num5': '',
            'Num6': '',
            'Num7': '',
            'Num8': '',
            'Num9': '',
            'Num10': '',
            'Num1': '',
            'NomeAtleta2': '',
            'NomeAtleta3': '',
            'NomeAtleta4': '',
            'NomeAtleta5': '',
            'NomeAtleta6': '',
            'NomeAtleta7': '',
            'NomeAtleta8': '',
            'NomeAtleta9': '',
            'NomeAtleta1': '',
            'LicAtleta2': '',
            'LicAtleta3': '',
            'LicAtleta4': '',
            'LicAtleta5': '',
            'LicAtleta6': '',
            'LicAtleta7': '',
            'LicAtleta8': '',
            'LicAtleta9': '',
            'LicAtleta10': '',
            'LicAtleta1': '',
            'IDAtleta1': '',
            'IDAtleta2': '',
            'IDAtleta3': '',
            'IDAtleta4': '',
            'IDAtleta5': '',
            'IDAtleta6': '',
            'IDAtleta7': '',
            'IDAtleta8': '',
            'IDAtleta9': '',
            'NomeAtleta10': '',
            'NomeDelegado1': '',
            'LicDelegado1': '',
            'NomeDelegado2': '',
            'LicDelegado2': '',
            'NomeTreinador': '',
            'LicTreinador': '',
            'NomeTreinadorAdj': '',
            'LicTreinadorAdj': '',
            'LicMedico': '',
            'NomeMedico': '',
            'LicMass': '',
            'NomeMass': '',
            'IDAtleta10': '',
            'NomeMec': '',
            'LicMec': '',
            'IDDelegado1': '',
            'IDDelegado2': '',
            'IDTreinadorAdj': '',
            'IDTreinador': '',
            'IDMed': '',
            'IDMass': '',
            'IDMec': '',
        }

        if self.competicao.designacao != False:
            dados['Compet'] = self.competicao.designacao
        if self.numero != False:
            dados['JogoNum'] = self.numero
        dados['Equipa'] = self.env['res.company'].browse(1).name
        dados['Data'] = self.start.split(' ')[0]

        info_atletas = list()
        for jogador in self.atletas:
            info_atletas.append((jogador.posicao, jogador.name, jogador.licencas_desportivas[0].numero, self.get_numcamisola(jogador)))

        i = 2
        gr = 1

        info_atletas.sort(key= lambda x:x[3] )
        for t in info_atletas:
            if t[0] == 'GR':
                na = 'NomeAtleta' + str(gr)
                la = 'LicAtleta' + str(gr)
                n = 'Num' + str(gr)
                dados[na] = t[1]
                dados[la] = t[2]
                if t[3] != 0:
                    dados[n] = t[3]
                gr = 10
            elif i<=9:
                na = 'NomeAtleta' + str(i)
                la = 'LicAtleta' + str(i)
                n = 'Num' + str(i)
                dados[na] = t[1]
                dados[la] = t[2]
                if t[3] != 0:
                    dados[n] = t[3]
                i += 1

        i = 1
        if self.treinador_principal.name != False:
            dados['NomeTreinador'] = self.treinador_principal.name
            if self.treinador_principal.licencas_desportivas:
                dados['LicTreinador'] = self.treinador_principal.licencas_desportivas[0].numero
            i = 2

        for treinador in self.treinador:
            if i == 2 and treinador.name != dados['NomeTreinador']:
                dados['NomeTreinadorAdj'] = treinador.name
                if treinador.licencas_desportivas:
                    dados['LicTreinadorAdj'] = treinador.licencas_desportivas[0].numero
            if i == 1 and self.treinador_principal.name == False:
                dados['NomeTreinador'] = treinador.name
                if treinador.licencas_desportivas:
                    dados['LicTreinador'] = treinador.licencas_desportivas[0].numero
                i += 1

        i = 1
        for seccionista in self.seccionistas:
            if i <= 2:
                na = 'NomeDelegado' + str(i)
                la = 'LicDelegado' + str(i)
                dados[na] = seccionista.name
                dados[la] = seccionista.licencas_desportivas[0].numero
                i += 1
        if self.massagista:
            dados['NomeMass'] = self.massagista.name
            dados['LicMass'] = self.massagista.licencas_desportivas[0].numero

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=ges.jogo&id=%s&filename=%s&info=%s' % (self.id,"convocatoria"+str(self.id)+".pdf", json.dumps(dados)),
            'target': 'self',
        }


    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        default['state'] = 'aberto'
        return super(Jogo, self).copy(default)

    @api.multi
    def name_get(self):
        repr = []
        for rec in self:
            if type(rec.em_casa) != bool and rec.em_casa == 's':
                if type(rec.equipa_adversaria.nome) != bool:
                    novo_nome = 'HCP - {}'.format(rec.equipa_adversaria.nome)
                else:
                    novo_nome = 'Jogo em casa'

            elif type(rec.em_casa) != bool and rec.em_casa == 'n':
                if type(rec.equipa_adversaria.nome) != bool:
                    novo_nome = '{} - HCP'.format(rec.equipa_adversaria.nome)
                else:
                    novo_nome = 'Jogo fora'
            else:
                novo_nome = 'Jogo'

            repr.append((rec.id, novo_nome))
        return repr

    @api.model
    def create(self, vals):
        vals['name'] = 'Jogo'
        res = super(Jogo, self).create(vals)
        res.write({
            'evento_ref': 'ges.jogo,' + str(res.id),
        })
        return res

    @api.multi
    def unlink(self):
        for rec in self:
            rec.evento_desportivo.unlink()
        return super(Jogo, self).unlink()
