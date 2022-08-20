# -*- coding: utf-8 -*-
{
    'name': "Reportes extra TM",
    'summary': """Modulo para reportes extras""",
    'description': """
                Permite imprimir reportes custom
        """,
    'author': "BulldogSoft/Kevin Cruz",
    'website': "http://www.bulldogsoft.com",
    'license': 'GPL-3',
    'category': 'Extra tools',
    'version': '0.1',
    'depends': ['base', 'purchase','account','stock','branch'],
    'data': [
        'report/po_tm.xml',
        'report/payment_recipt.xml',
        'report/r_mercaderia.xml',
        'report/reportes_config.xml',
        'views/invoice_view.xml',
        'wizard/reporte_bodegas.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
