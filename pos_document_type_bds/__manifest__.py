# -*- coding: utf-8 -*-
#################################################################################
{
   'name':"Pos Document Type",
   'author':"Bulldogsoft/Kevin Cruz",
   'category':"Point of Sale",
   'summary':"""" Permite elegir el tipo de documento y asignarle una secuencia """,
   'website':"http://www.bulldogsoft.com",
   'description':""" Permite elegir el tipo de documento y asignarle una secuencia""",
   'version' : '14.0.0',
   'depends' : ['account', 'point_of_sale',],
   'data':[
            'views/pos.xml',
            'views/pos_assets.xml',
            'views/doctype_view.xml',
            'security/ir.model.access.csv'
   ],
   'qweb': [
        'static/src/xml/pos_buttons.xml',
        'static/src/xml/doc_button.xml',
    ],
    'license'     : 'AGPL-3',
    'installable':True,
    'application':True,
    'auto_install':False,
}
