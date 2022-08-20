# -*- coding: utf-8 -*-
{
    'name': 'Customer Search Filter',
    'author': 'Bulldogsoft',
    'category': 'Sales',
    'license': 'AGPL-3',
    'website': 'soporte@bulldogsoft.com',
    'version': '14.0.1.0.1',
    'summary': '''
                Filtros de clientes en ventas por nrc, nit, giro
            ''',
    'description': '''
                   Filtros de clientes en ventas por nrc, nit, giro
                ''',
    'depends': ['base'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'images': [
        'static/description/banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
