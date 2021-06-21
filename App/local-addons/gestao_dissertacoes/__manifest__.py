{
    'name': "Gestão de Dissertações",
    'summary': "Add on para gerir o processo de defesa da dissertação de um aluno",
    'sequence': -100,
    'description': """
        Write some description
    """,
    'author': "Joel Ferreira, João Linhares, Rui Azevedo",
    'category': 'Processo',
    'version': '1.0.0',
    'depends': ['base', 'report_py3o', 'mail'],
    'license': "LGPL-3",
    'data': [
             'security/funcionario_security.xml',
             'security/ir.model.access.csv',
             'views/gestao_diss_processo.xml',
             'views/gestao_diss_membro.xml',
             'views/gestao_diss_filiacao.xml',
             'views/gestao_diss_curso.xml',
             'views/gestao_diss_ano_letivo.xml',
             'views/gestao_diss_categoria.xml',
             'views/gestao_diss_dashboard.xml',
             'views/invite_template.xml',
			 'reports/report_ata_primeira_reuniao.xml',
             'data/convite_presidente.xml',
             'data/convite_arguente.xml',
             'data/convite_vogal.xml',
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
