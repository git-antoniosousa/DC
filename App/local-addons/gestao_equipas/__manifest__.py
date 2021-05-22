{
    'name': "Gestão de equipas desportivas",

    'summary': """
        Aplicação para a gestão das atividades de formação e competição de uma equipa desportiva.""",

    'description': """
        Aplicação para a gestão das atividades de formação e competição de uma equipa desportiva, com suporte para:
            - **Gestão de atletas**
                - Exames médicos
                - Licenças desportivas
                - Evolução de dados físicos
                - Gestão de esforços
                - Registo lesões
            - **Gestão de sócios**
            - **Gestão de secionistas**
            - **Gestão de treinadores**
            - **Gestão de treinos e jogos**
                - Planeamento de treinos
                - Presenças em treinos e jogos
                - Convocatórias para jogos e treinos
            - **Dados estatisticos**""",
    'author': "André Santos, Diogo Machado, Rui Leite",

    'application': True,
    'auto_install': True,
    'category': 'Admininstration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'google_calendar', 'product', 'account', 'fetchmail', 'board'],

    # always loaded
    'data': [
        'security/ges_security.xml',
        'security/ir.model.access.csv',
        'reports/report_horario_generate.xml',
        'reports/report_horario_atleta_generate.xml',
        'reports/report_horario_treinador_generate.xml',
        'reports/report_horario_seccionista_generate.xml',
        'reports/report_mapa_generate.xml',
        'reports/report_reg_presencas_generate.xml',
        'reports/report_folha_convoc_generate.xml',
        'reports/report_presencas_geral_generate.xml',
        'reports/report_presencas_atleta_generate.xml',
        'reports/report_carga_fisica_generate.xml',
        'wizards/horario_report.xml',
        'wizards/carga_fisica_report.xml',
        'wizards/presencas_report.xml',
        'data/socio_sequencia.xml',
        'views/tempo_parte.xml',
        'views/dados_antropometricos.xml',
        'views/testes_fisicos.xml',
        'views/registos_carga_fisica.xml',
        'views/partner.xml',
        'views/atletas.xml',
        'views/competicao.xml',
        'views/eventos_jogos.xml',
        'views/seccionistas.xml',
        'views/massagistas.xml',
        'views/treinadores.xml',
        'views/escaloes.xml',
        'views/licencas_desportivas.xml',
        'views/locais.xml',
        'views/epocas.xml',
        'views/categorias_treino.xml',
        'views/equipas.xml',
        'views/equipa_adversaria.xml',
        'views/planeamento.xml',
        'views/treino.xml',
        'views/pai.xml',
        'views/subscricoes.xml',
        'views/faturas.xml',
        'views/jogo.xml',
        'views/eventos_calendario.xml',
        'views/tipo_lesao.xml',
        'views/lesoes.xml',
        'views/zonas.xml',
        'views/menus.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/subscricoes.xml',
        'demo/tempo_partes.xml',
        'demo/tipo_lesao.xml',
        'demo/company.xml',
        'demo/epocas.xml',
        'demo/competicoes.xml',
        'demo/equipas_adversarias.xml',
        'demo/escaloes.xml',
        'demo/locais.xml',
        'demo/categorias_treino.xml',
        'demo/atletas.xml',
        'demo/pais.xml',
        'demo/equipas.xml',
        'demo/seccionistas.xml',
        'demo/treinadores.xml',
        'demo/planeamento.xml',
        'demo/zonas.xml'

    ],
}
