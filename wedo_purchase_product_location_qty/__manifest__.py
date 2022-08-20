# Copyright 2020 Bulldogsoft

{
    'name': "Cantidades disponibles-Compras-BDS",
    'version': '14.0.1.0',
    'license': 'OPL-1',
    'author': 'Bulldogsoft-Gerson Carranza',
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
    'images': ['images/main_screenshot.png'],
    'data': [
        'views/purchase_view.xml',
        'views/templates.xml',
    ],
    'qweb': ['static/src/xml/qty_at_date.xml'],
    'application': True,
}

