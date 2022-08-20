# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class StockPiking(models.Model):
    _inherit = "stock.picking"

    @api.onchange('move_ids_without_package')
    def validate_quantity_done(self):
        for rec in self.move_ids_without_package:
            if rec.quantity_done > rec.product_uom_qty:
                raise UserError(
                    'La cantidad Hecha en él (Producto: %s) no puede ser mayor a la cantidad demandada'
                    % rec.product_id.name)
 

class StockMove(models.Model):
    _inherit = "stock.move"

    @api.onchange('product_uom_qty', 'quantity_done')
    def validate_quantity_done_sm(self):
        for rec in self:
            if rec.quantity_done > rec.product_uom_qty:
                raise UserError(
                    'La cantidad Hecha en él (Producto: %s) no puede ser mayor a la cantidad demandada'
                    % rec.product_id.name)                


