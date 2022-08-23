# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        if not self.order_line:
            raise ValidationError('Necesita agregar un producto antes de validar')
        return super(SaleOrder, self).action_confirm()




