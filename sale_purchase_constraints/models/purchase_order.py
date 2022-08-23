# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        if not self.order_line:
            raise ValidationError('Necesita agregar un producto antes de validar')
        return super(PurchaseOrder, self).button_confirm()




