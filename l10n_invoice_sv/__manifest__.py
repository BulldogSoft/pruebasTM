# -*- coding: utf-8 -*-
{
    'name': "Facturacion de El Salvador",
    'summary': """Facturacion de El Salvador""",
    'description': """
       Facturacion de El Salvador.
       Permite Imprimir los tres tipos de facturas utilizados en El Salvador
        - Consumidor Final
        - Credito Fiscal
        - Exportaciones
      Tambien permite imprimir los documentos que retifican:
        - Anulaciones.
        - Nota de Credito
        - Anulaciones de Exportacion
      Valida que todos los documentos lleven los registros requeridos por ley
        """,
    'author': "BulldogSoft (Guillermo Guevara)",
    'website': "http://www.bulldogsoft.com",
    'price': 150.00,
    'currency': 'USD',
    'license': 'GPL-3',
    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Contabilidad',
    'version': '0.5',
    # any module necessary for this one to work correctly
    'depends': ['base', 'l10n_sv', 'account', 'account_accountant'],
    # always loaded
    'data': [
        'views/account_journal.xml',
        'views/account_invoice_view.xml',
        'views/account_invoice_proveedor_view.xml',
        'views/amount_word_view.xml',
        'data/journal_data.xml',
        'report/report_invoice_anu.xml',
        'report/report_invoice_ccf.xml',
        'report/report_invoice_fcf.xml',
        'report/report_invoice_exp.xml',
        'report/report_invoice_ndc.xml',
        'report/report_quedan.xml',
        'report/report_invoice_all_in_one_bds.xml',
        'report/report_invoice_se.xml',
        'report/invoice_report.xml',
        'report/report_invoice_main.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    #'demo.xml',
    'installable': True,
    'application': False,
    'auto_install': False,
    'post_init_hook': 'invoices_refunds',
}
