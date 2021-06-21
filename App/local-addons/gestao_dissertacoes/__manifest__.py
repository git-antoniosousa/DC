{
    'name': "Gestão de Dissertações",
    'summary': "Add on para gerir o processo de defesa da dissertação de um aluno",
    'sequence': -100,
    'description': """
        Aplicação para gerir todo o processo de defesa da Dissertação dos alunos do
        departamento de Informática da Universidade do Minho. O objetivo desta aplicação
        é automatizar este processo e descomplicar grande parte das tarefas monótonas.
    """,
    'author': "Joel Ferreira, João Linhares, Rui Azevedo",
    'category': 'Gestão',
    'version': '1.0.0',
    'depends': ['base', 'report_py3o'],
    'license': "LGPL-3",
    'data': [
        ############################# VIEWS #############################
        'views/gestao_diss_processo.xml',
        'views/gestao_diss_membro.xml',
        'views/gestao_diss_filiacao.xml',
        'views/gestao_diss_curso.xml',
        'views/gestao_diss_categoria.xml',
        'views/gestao_diss_dashboard.xml',
        'views/invite_template.xml',

        ######################## REPORT'S PDF ############################
        'reports/pdf/report_proposta_juri.xml',
        'reports/pdf/report_formulario_candidato_pt.xml',
        'reports/pdf/report_formulario_candidato_eng.xml',
        'reports/pdf/report_ata_primeira_reuniao.xml',

        ######################## REPORT'S ODT ############################
        'reports/odt/report_proposta_juri.xml',
        'reports/odt/report_formulario_candidato_pt.xml',
        'reports/odt/report_formulario_candidato_eng.xml',
        'reports/odt/report_ata_primeira_reuniao.xml',
        'reports/odt/report_ata_provas.xml',

        ############################ WIZARDS #############################
        'wizards/gerar_proposta_juri_wizard.xml',
        'wizards/gerar_form_candidato_wizard.xml',
        'wizards/gerar_ata_provas.xml',
        'wizards/gerar_ata_primeira_reuniao.xml',
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
