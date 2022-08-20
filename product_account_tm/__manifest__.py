{
    'name': 'Product Custom Accounts - TM',
    'version': '12.0.0.0',
    'summary': """ 
            Módulo para poner cuentas contables personalizadas en impuestos, productos y servicios desde la opción 
            de branch, estas podrán ser distintas dependiendo de la branch del usuario
    """,
    'category': 'Extra tools',
    'author': "BulldogSoft / Gerson Carranza",
    'website': "https://bulldogsoft.odoo.com",
    'license': 'AGPL-3',
    'depends': ['base', 'branch', 'stock', 'account', 'sale_management', 'contact_data_tm'],
    'data': [
        'views/branch_inhertited_view.xml',
    ],
    'installable': True,
}