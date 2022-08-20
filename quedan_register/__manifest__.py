# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Resgistro de Quedan',
    'author': 'Bulldogsoft',
    'summary': 'Modulo para llevan un registro de los quedans realizados',
    'category': 'Extra Tools',
    'depends': ['base', 'account', 'bi_is_customer_is_vendor', 'branch'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/quedan_register_pro_view.xml',
        'report/invoice_report.xml',
        'report/report_invoice_main.xml',
        'report/report_quedan.xml',
        'wizard/print_invoice_quedan_view.xml',
    ],
    'installable': True,
    'application': True,
}
