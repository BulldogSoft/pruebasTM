# Copyright 2020 Bulldogsoft
from odoo import models, fields
from dateutil.relativedelta import relativedelta
from datetime import datetime

class StockMove(models.Model):
    _inherit = 'stock.move'

    def bds_show_stock(self):
        """ Returns an action that will open a form view (in a popup) allowing to work on all the
        move lines of a particular move. This form view is used when "show operations" is not
        checked on the picking type.
        """
        self.ensure_one()
        view = self.env.ref('picking_product_location_qty_bds.stock_consult').id

        return {
            'name': ('Stock Disponible'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'stock.quant',
            'views': [(view, 'tree')],
            'view_id': view,
           # 'view_id': False,
            'target': 'new',
            'domain': [("product_id", '=', self.product_id.id),('location_id.usage','=','internal')],
            'res_id': self.id,
        }

