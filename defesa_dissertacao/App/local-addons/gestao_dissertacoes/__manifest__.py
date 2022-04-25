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
    'category': 'Processo',
    'version': '1.0.0',
    'depends': ['base', 'report_py3o', 'mail',],
    'license': "LGPL-3",
    'data': [
        ########################## SECURITY #############################
        'security/funcionario_security.xml',
        'security/ir.model.access.csv',

        ############################# VIEWS #############################
        'views/gestao_diss_processo.xml',
        'views/gestao_diss_membro.xml',
        'views/gestao_diss_filiacao.xml',
        'views/gestao_diss_curso.xml',
        'views/gestao_diss_ano_letivo.xml',
        'views/gestao_diss_categoria.xml',
        'views/gestao_diss_dashboard.xml',
        'views/invite_template.xml',


        ######################## REPORT'S PDF ############################
        'reports/pdf/report_proposta_juri.xml',
        'reports/pdf/report_formulario_candidato_pt.xml',
        'reports/pdf/report_formulario_candidato_eng.xml',
        'reports/pdf/report_ata_primeira_reuniao.xml',
        'reports/pdf/report_justificacao_arguente.xml',

        ######################## REPORT'S ODT ############################
        'reports/odt/report_proposta_juri.xml',
        'reports/odt/report_formulario_candidato_pt.xml',
        'reports/odt/report_formulario_candidato_eng.xml',
        'reports/odt/report_ata_primeira_reuniao.xml',
        'reports/odt/report_ata_provas.xml',
        'reports/odt/report_justificacao_arguente.xml',

        ############################ WIZARDS #############################
        'wizards/gerar_proposta_juri_wizard.xml',
        'wizards/gerar_form_candidato_wizard.xml',
        'wizards/gerar_ata_provas.xml',
        'wizards/gerar_ata_primeira_reuniao.xml',
        'wizards/gerar_justificacao_arguente.xml',

        ############################# EMAILS #############################
		'data/convite_presidente.xml',
        'data/convite_arguente.xml',
        'data/convite_vogal.xml',
        'data/convocatoria_aluno.xml',
        'data/convocatoria_arguente.xml',
        'data/convocatoria_presidente.xml',
        'data/convocatoria_vogal.xml',
        'data/ata_primeira_reuniao.xml',
        'data/declaracao_aluno.xml',
        'data/ata_prova.xml',
        'data/ata_sequence.xml',
        'data/envio_convocatoria.xml',
        'data/envio_declaracao_arguente.xml',
        'data/envio_pedido_assinatura.xml',
        'data/envio_pedido_link.xml',
        'data/pedido_anexos.xml',
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
