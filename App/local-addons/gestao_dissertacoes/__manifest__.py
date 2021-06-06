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
    'depends': ['base', 'report_py3o', 'mail'],
    'license': "LGPL-3",
    'data': [
             'views/gestao_diss_processo.xml',
             'views/gestao_diss_membro.xml',
             'views/gestao_diss_filiacao.xml',
             'views/gestao_diss_curso.xml',
             'views/gestao_diss_categoria.xml',
             'views/gestao_diss_dashboard.xml',
             'views/invite_template.xml'
             ],
    'demo': [
        #'demo/alunos.xml',
        #'demo/processos.xml'
    ],
    'css': [
        'static/src/css/aluno.css',
        'static/src/css/processo.css'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
