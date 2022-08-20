# -*- coding: utf-8 -*-
{
    'name': "Retaceo SV",
    'author': "BulldogSoft",
    'website': "http://www.bulldogsoft.com",
    'category': 'Inventario - Compras',
    'version': '0.5',
    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'stock', 'account'],
    # always loaded
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'report/report.xml',
        'report/report_main.xml',
        'report/report_retaceo.xml',
        'views/retaceo_view.xml',
        'views/product_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [],
    #'demo.xml',
    'installable': True,

}
