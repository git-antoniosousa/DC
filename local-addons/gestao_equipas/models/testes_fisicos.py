# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class TestesFisicos(models.Model):
    _name = 'ges.testes_fisicos'
    _description = 'Testes Fisicos'
    _order = 'data'

    atleta_id = fields.Many2one('ges.atleta', 'Atleta', ondelete='cascade', required=True)
    # Dados gerais
    data = fields.Date('Data de realização', required=True, default=datetime.date.today())

    velocidadesapatilhas = fields.Float(string='Velocidade Sapatilhas (20m)(s)', default=None,
                            digits=(3, 3), group_operator="avg")

    velocidadepatins = fields.Float(string='Velocidade Patins (20m)(s)', default=None,
                                     digits=(3, 3), group_operator="avg")

    agilidadepatins = fields.Float(string='Agilidade Patins, com stick e bola (20+10+10+20+5+5)', default=None,
                                     digits=(3, 3), group_operator="avg")

    circuitopatins = fields.Float(string='Circuito Patins, com stick e bola', default=None,
                                    digits=(3, 3), group_operator="avg")

    vaivem = fields.Float(string='Vaivém (FitEscola)', default=None,
                                   digits=(3, 3), group_operator="avg", help="http://fitescola.dge.mec.pt/media/testesDocs/2_doc_descrtestes_vaivem.pdf")

    abdominais= fields.Integer(string='Abdominais (FitEscola)', default=None,
                           group_operator="avg",  help="http://fitescola.dge.mec.pt/media/testesDocs/7_doc_descrtestes_abd.pdf")

    flexoesbracos = fields.Integer(string='Flexões de braços (FitEscola)', default=None,
                              group_operator="avg", help="http://fitescola.dge.mec.pt/media/testesDocs/8_doc_descrtestes_flexbr.pdf")

    impulsaohorizontal = fields.Integer(string='Impulsão horizontal (FitEscola)', default=None,
                                group_operator="avg", help="http://fitescola.dge.mec.pt/media/testesDocs/9_doc_descrtestes_imphor.pdf")

    impulsaovertical = fields.Float(string='Impulsão vertical (FitEscola)', default=None,
                                      digits=(3, 2), group_operator="avg",help="http://fitescola.dge.mec.pt/media/testesDocs/10_doc_descrtestes_impvert.pdf")

    flexibilidadeombrodireito = fields.Boolean(string='Flexibilidade do ombro direito (FitEscola)', default=None,
                                     group_operator="avg", help="http://fitescola.dge.mec.pt/media/testesDocs/11_doc_descrtestes_flexomb.pdf")

    flexibilidadeombroesquerdo = fields.Boolean(string='Flexibilidade do ombro esquerdo (FitEscola)', default=None,
                                            group_operator="avg", help="http://fitescola.dge.mec.pt/media/testesDocs/11_doc_descrtestes_flexomb.pdf")

    flexibilidademembroinferiordireito = fields.Float(string='Flexibilidade do membro inferior direito (FitEscola)', default=None,
                                       digits=(3, 2), group_operator="avg", help="http://fitescola.dge.mec.pt/media/testesDocs/12_doc_descrtestes_flexmembinf.pdf")

    flexibilidademembroinferioresquerdo = fields.Float(string='Flexibilidade do membro inferior esquerdo (FitEscola)',
                                                      default=None,
                                                      digits=(3, 2), group_operator="avg", help="http://fitescola.dge.mec.pt/media/testesDocs/12_doc_descrtestes_flexmembinf.pdf")
