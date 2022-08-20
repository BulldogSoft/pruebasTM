    # -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    credit_account_id = fields.Many2one('account.account', string="Cta. Crédito Retaceo")
    debit_account_id = fields.Many2one('account.account', string="Cta. Débito Retaceo")


class ProductProduct(models.Model):

    _inherit = 'product.product'

    credit_account_id = fields.Many2one('account.account', string="Cta. Crédito Retaceo")
    debit_account_id = fields.Many2one('account.account', string="Cta. Débito Retaceo")