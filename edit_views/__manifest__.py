# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Modificación de Vistas',
    'author': 'BDS/Gerson Carranza',
    'summary': 'Modulo para modificar vistas en Tienda Morena',
    'category': 'Extra Tools',
    'depends': ['base', 'sale_management'],
    'data': [
        'views/sale_order_view_inherited.xml',
    ],
    'installable': True,
    'application': True,
}
