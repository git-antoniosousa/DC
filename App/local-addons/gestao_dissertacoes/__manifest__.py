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
    'depends': ['base', 'report_py3o'],
    'depends': ['base',],
    'license': "LGPL-3",
    'data': [
             'reports/doc_homologacao_report.xml',
             'views/gestao_diss_processo.xml',
             'views/gestao_diss_membro.xml',
             #'views/gestao_diss_docente.xml',
             'views/gestao_diss_dashboard.xml'
             ],
    'demo': [
        'demo/alunos.xml',
        'demo/processos.xml'
    ],
    'css': [
        'static/src/css/aluno.css'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
