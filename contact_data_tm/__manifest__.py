# copyright 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'TechData - TM',
    'version': '12.0.0.0',
    'category': 'Extra tools',
    'author': "BulldogSoft / Gerson Carranza",
    'website': "https://bulldogsoft.odoo.com",
    'license': 'AGPL-3',
    'depends': ['base', 'stock', 'hr', 'purchase', 'account', 'contribuyente_partner_type'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_type_view.xml',
        'views/product_inhertited_view.xml',
        'views/extra_fields_view.xml',
    ],
    'installable': True,
}