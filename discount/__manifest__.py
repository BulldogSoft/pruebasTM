# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Discount Approval',
    'price': 145.0,
    'currency': 'USD',
    'version': '13.0.0.0.0',
    'category': 'Sales',
    'license': 'Other proprietary',
    'sequence': 3,
    'summary': 'Sale Discount Approval',
    'description': """
            """,
    'author': 'FOSS INFOTECH PVT LTD',
    'website': 'https://www.fossinfotech.com',
    'depends': ['sale','sale_management'],
    'data': [
            'security/ir.model.access.csv',
            'data/mail_template_data.xml',
            'views/sale.xml',
    ],
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/index.html',
    ],
  
    'installable': True,
    'auto_install': True,
    'application': True,
}
