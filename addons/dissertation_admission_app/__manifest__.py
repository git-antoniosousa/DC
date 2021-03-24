{'name': 'Aplicação para Admissão a Dissertação',
 'description': 'Gestão do processo de admissão à dissertação',
 'depends': ['base'],
 'data': [
    'security/dissertation_admission_security.xml',
    'security/ir.model.access.csv',
    'views/dissertation_admission_menu.xml',
    #'views/dissertation_list_template.xml',
    #'views/dissertation_view.xml',
 ],
 'application': True,
 'installable': True,
 }
