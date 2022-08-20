from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    documento_fiscal = fields.Selection(string='Documento fiscal',
                                        selection=[('ccf', 'CCF'),
                                                   ('fcf', 'FCF'),
                                                   ('ticket', 'Ticket'),
                                                   ], required=False, default='ticket')
