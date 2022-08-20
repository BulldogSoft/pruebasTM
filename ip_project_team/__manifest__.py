# -*- coding: utf-8 -*-
{
    'name': 'Project Team',
    'summary': "Manage Project & Task with Project Team",
    'description': "Manage Project & Task with Project Team",

    'author': 'iPredict IT Solutions Pvt. Ltd.',
    'website': 'http://ipredictitsolutions.com',
    'support': 'ipredictitsolutions@gmail.com',

    'category': 'Project',
    'version': '14.0.0.1.0',
    'depends': ['project'],

    'data': [
        'security/ir.model.access.csv',
        'security/team_security.xml',
        'views/project_team_view.xml',
        'views/project_project_view.xml',
        'views/project_task_view.xml',
    ],

    'license': "OPL-1",
    'price': 17,
    'currency': "EUR",

    'auto_install': False,
    'installable': True,

    'images': ['static/description/banner.png'],
    'pre_init_hook': 'pre_init_check',
}
