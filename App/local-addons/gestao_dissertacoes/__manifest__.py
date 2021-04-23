{
    'name': "Gestão de Dissertações",
    'summary': "Add on para gerir o processo de defesa da dissertação de um aluno",
    'sequence': -100,
    'description': """
        Write some description
    """,
    'author': "Joel Ferreira, João Linhares, Rui Azevedo",
    'category': 'Uncategorized',
    'version': '1.0.0',
    'depends': ['base'],
    'license': "LGPL-3",
    'data': ['views/gestao_diss_processo.xml',
             'views/gestao_diss_arguente.xml',
             'views/gestao_diss_docente.xml',
             'views/gestao_diss_dashboard.xml',
             'views/gestao_diss_entidade_patronal.xml'
             ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}