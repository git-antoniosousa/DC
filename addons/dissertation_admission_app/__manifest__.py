{'name': 'Aplicação para Admissão a Dissertação',
 'description': 'Gestão do processo de admissão à dissertação',
 'depends': ['base'],
 'data': [
     'security/dissertation_admission_security_groups.xml',
     'security/dissertation_admission_security_rules.xml',
     'security/ir.model.access.csv',
     'views/dissertation_admission_menu.xml',
     'views/user_view.xml',
     'views/student_view.xml',
 ],
 'application': True,
 'installable': True,
 }
