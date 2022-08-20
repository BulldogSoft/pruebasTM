#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2019 BulldogSoft All Rights Reserved.
# Guillermo Guevara, Gerson Carranza - BulldogSoft
# (http://www.BulldogSoft.com)

#
# This module provides a minimal Salvadorean chart of accounts that can be use
# to build upon a more complex one.  It also includes a chart of taxes and
# the Dollar currency.
#
# This module works with Odoo 13.0
#

{
    'name': 'El Salvador - Accounting',
    'version': '1.0',
    'category': 'Localization',
    'description': """
This is the base module to manage the accounting chart for El Salvador.
==================================================================================

Agrega una nomenclatura contable para El Salvador. También icluye impuestos y
la moneda del dollar. -- Adds accounting chart for El Salvador. It also includes
taxes and the Dollar currency.""",
    'author': 'Guillermo Guevara & Gerson Carranza',
    'website': 'http://BulldogSoft.com/',

    'depends': ['base', 'account', 'phone_validation', 'journal_sequence'],

    'data': [
        'views/view_res_company.xml',
        'views/view_res_partner.xml',
        'data/l10n_sv_chart_data.xml',
        'data/account.account.template.csv',
        'data/l10n_sv_chart_post_data.xml',
        'data/account_data.xml',
        'data/account_tax_data.xml',
        'data/account_fiscal_position.xml',
        'data/account_chart_template_data.xml',
        'data/sequence_data.xml',
        'data/journal_data.xml',
    ],
     # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'post_init_hook': 'drop_journal',
}
