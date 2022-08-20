# -*- coding: utf-8 -*-
{
    'name': "Reportes de Facturacion de El Salvador TM",
    'summary': """Reportes de Facturacion de El Salvador""",
    'description': """
           Agrega los reportes de facturación 
        """,
    'author': "BulldogSoft/Kevin Cruz",
    'website': "http://www.bulldogsoft.com",
    'license': 'GPL-3',
    'category': 'Contabilidad',
    'version': '0.5',
    'depends': ['account', 'l10n_invoice_sv'],
    # always loaded
    'data': [
        #configuraciones
        'report/configuraciones/invoice_report.xml',
        'report/configuraciones/template_css.xml',
        'report/configuraciones/report_invoice_main.xml',
        #unico
        'report/unico/report_invoice_unico_tm.xml',
        'report/sujeto_excluido/se_template.xml',
        #views
        'views/botones.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': False,
    'auto_install': False,

}
