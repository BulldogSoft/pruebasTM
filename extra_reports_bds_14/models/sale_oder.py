from odoo import fields, models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    concepto_factura = fields.Char(string="Concepto de Factura",  required=False, readonly=False)