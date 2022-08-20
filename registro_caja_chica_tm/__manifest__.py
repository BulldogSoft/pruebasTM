# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Resgistro de Caja Chica',
    'author': 'BDS/Gerson carranza',
    'summary': 'Modulo para llevan un registro de recibos caja chica',
    'category': 'Extra Tools',
    'depends': ['base', 'account', 'bi_is_customer_is_vendor'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'report/report.xml',
        'report/report_caja_chica.xml',
        'report/report_main.xml',
        'views/caja_chica_tm_view.xml',
    ],
    'installable': True,
    'application': True,
}
