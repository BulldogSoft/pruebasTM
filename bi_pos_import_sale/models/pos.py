from datetime import datetime, timedelta, date
import dateutil.parser
from itertools import groupby
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
from odoo.tools import html2plaintext
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    documento_fiscal = fields.Selection(string='Documento fiscal',
                                        selection=[('ccf', 'CCF'),
                                                   ('fcf', 'FCF')
                                                   ], required=False)


class PosConfiguration(models.Model):
    _inherit = 'pos.config'

    check = fields.Boolean(string='Import Sale Order', default=False)
    load_orders_days = fields.Integer('Load Orders of Last Days')
    load_draft_sent = fields.Boolean(string='Load only draft/sent sale orders', default=False)
    cancle_order = fields.Boolean(string='Cancel Sale Order after Import', default=False)


class InheritPOSOrder(models.Model):
    _inherit = 'pos.order'
    sale_order_ids = fields.Many2many('sale.order', string="Imported Sale Order(s)")

    def _order_fields(self, ui_order):
        res = super(InheritPOSOrder, self)._order_fields(ui_order)
        config = self.env['pos.session'].browse(ui_order['pos_session_id']).config_id

        if 'imported_sales' in ui_order and ui_order.get('imported_sales'):
            so = ui_order['imported_sales'].split(',')
            so.pop()
            so_ids = []
            sale_orders = []
            for odr in so:
                sale = self.env['sale.order'].browse(int(odr))
                if sale:
                    so_ids.append(sale.id)
                    sale_orders.append(sale)
            res.update({
                'sale_order_ids': [(6, 0, so_ids)]
            })

        if config.cancle_order:
            for s in sale_orders:
                s.action_cancel()

        return res
