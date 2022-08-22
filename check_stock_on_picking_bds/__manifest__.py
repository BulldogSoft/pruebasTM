# Copyright 2020 Bulldogsoft

{
    'name': "Stock disponible desde picking",
    'version': '14.1',
    'license': 'OPL-1',
    'author': 'Bulldogsoft/Kevin Cruz',
    'support': 'hello@bulldogsoft.com',
    'category': 'purchase',
    'sequence': 1,
    'depends': ['purchase','stock'],
    'summary': """
      Muestra las cantidades disponibles segun las bodegas que tiene configurada la empresa
       """,
    'description': """
    Muestra las cantidades disponibles segun las bodegas que tiene configurada la empresa
        """,
    'data': [
        'views/picking_view.xml',
        'views/templates.xml',
    ],
    'qweb': ['static/src/xml/qty_at_date.xml'],
    'application': True,
}

