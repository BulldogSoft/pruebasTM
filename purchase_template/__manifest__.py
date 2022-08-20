# -*- coding: utf-8 -*-
# Copyright 2020 Bulldogsoft

{
    'name': "Plantillas de Compras",
    'version' : '14.0.1.0',
	'license' : 'OPL-1',
	'author': 'Bulldogsoft-Gerson Carranza',
	'support' : 'hello@bulldogsoft.com',
    'category': 'purchases',
    'sequence': 1,
    'website' : 'http://bulldogsoft.com',
    'description': """
	Puedes crear tus plantillas personalizadas para tus proveedores.
    """,
    'depends': ['purchase'],
	'images': ['images/main_screenshot.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_template_views.xml',
    ],
    'demo': [
    ],
}
