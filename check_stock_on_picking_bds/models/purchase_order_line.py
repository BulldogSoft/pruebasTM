# Copyright 2020 Bulldogsoft
from odoo import models, fields
from dateutil.relativedelta import relativedelta
from datetime import datetime


class StockMove(models.Model):
    _inherit = 'stock.move'
    product_stock_quant_ids = fields.One2many('stock.quant', 'product_id', related='product_id.stock_quant_ids')

    def product_info(self, product_id, product_stock_quant_ids):
        locations = self.env['stock.location'].search_read([('usage', '=', 'internal')], ['id', 'name'])
        data = []
        total = {'qty': 0}
        for location in locations:
            domain = [('id', 'in', [quant_id for quant_id in product_stock_quant_ids]),
                      ('location_id', '=', location['id']), ]
            quant = self.env['stock.quant'].search_read(domain, ['quantity'])
            qty = quant and quant[0]['quantity'] or 0
            data.append({'name': location['name'], 'qty': qty})
            total['qty'] += qty
        data.append({'name': 'Total', 'qty': total['qty']})
        return data
