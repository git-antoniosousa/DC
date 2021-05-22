# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class DadosAntropometricos(models.Model):
    _name = 'ges.dados_antropometricos'
    _description = 'Dados Antropometricos'
    _order = 'data'

    atleta_id = fields.Many2one('ges.atleta', 'Atleta', ondelete='cascade', required=True)
    # Dados gerais
    data = fields.Date('Data de realização', required=True, default=datetime.date.today())

    estatura = fields.Float(string='Estatura (cm)', default=None,
                            digits=(3, 2), group_operator="avg")

    altura_sentado = fields.Float(string='Altura sentado (cm)',
                                  digits=(3, 2), group_operator="avg")

    envergadura = fields.Float(string='Envergadura (cm)',
                               digits=(3, 2), group_operator="avg")
    massa_corporal = fields.Float(string='Massa Corporal (Kg)',
                                  digits=(3, 2), group_operator="avg")

    # Comprimentos
    ms_direito = fields.Float(string='Membro Superior Direito',
                              digits=(3, 2))

    ms_esquerdo = fields.Float(string='Membro Superior Esquerdo',
                               digits=(3, 2))

    mi_direito = fields.Float(string='Membro Inferior Direito',
                              digits=(3, 2))

    mi_esquerdo = fields.Float(string='Membro Inferior Esquerdo',
                               digits=(3, 2))

    braco_direito = fields.Float(string='Braço Direito',
                                 digits=(3, 2))

    braco_esquerdo = fields.Float(string='Braço Esquerdo',
                                  digits=(3, 2))

    antebraco_direito = fields.Float(string='Antebraço Direito',
                                     digits=(3, 2))

    antebraco_esquerdo = fields.Float(string='Antebraço Esquerdo',
                                      digits=(3, 2))

    mao_direita = fields.Float(string='Mão direita',
                               digits=(3, 2))

    mao_esquerda = fields.Float(string='Mão esquerda',
                                digits=(3, 2))

    # Perimetros
    perimetro_abdominal = fields.Float(string='Abdominal',
                                       digits=(3, 2))

    anca_quadril = fields.Float(string='Anca/Quadril',
                                digits=(3, 2))

    # Diâmetro
    palmar = fields.Float(string='Palmar',
                          digits=(3, 2))
    biacromial = fields.Float(string='Biacromial',
                              digits=(3, 2))

    # Pregas
    tricipital = fields.Integer(string='Tricipital')
    bicipital = fields.Integer(string='Bicipital')
    subscapular = fields.Integer(string='Subcapsular')
    suprailiaca = fields.Integer(string='Suprailiaca')
    prega_abdominal = fields.Integer(string='Abdominal')
    crural_anterior = fields.Integer(string='Crural anterior')
    geminal_medial = fields.Integer(string='Geminal medial')