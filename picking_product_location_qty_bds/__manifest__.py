# Copyright 2020 Bulldogsoft

{
    'name': "Cantidades disponibles en Picking",
    'version': '14.0.1.0',
    'license': 'OPL-1',
    'author': 'Bulldogsoft/Kevin Cruz',
    'support': 'hello@bulldogsoft.com',
    'sequence': 1,
    'depends': ['stock'],
    'summary': """
      Muestra las cantidades disponibles segun las bodegas que tiene configurada la empresa
       """,
    'description': """
    Muestra las cantidades disponibles segun las bodegas que tiene configurada la empresa
        """,
    'data': [
        'views/picking_view.xml',
    ],
    'installable': True,
    'application': True,
}

