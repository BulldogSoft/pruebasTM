# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class InvoiceOrder(models.Model):

    _inherit = 'account.move'

    def _compute_amount_in_word(self):
        for rec in self:
            rec.num_word = str(rec.currency_id.amount_to_text(rec.amount_total))

    num_word = fields.Char(string="Monto:", compute='_compute_amount_in_word')

    tipo_retencion = fields.Selection(string="Retención",
                                      selection=[('0', 'Sin Retención'),
                                                 ('1', 'Retención 1%'),
                                                 ], required=False, default='0')

    ref_retencion = fields.Char(string="No. de Documento de Retención", required=False,)
