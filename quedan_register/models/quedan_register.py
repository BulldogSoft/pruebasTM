# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class ProductTemplate(models.Model):
    _name = "quedan.register"

    fecha = fields.Date(string="Fecha", required=False, )
    empresa = fields.Many2one('res.partner', string='Empresa', domain="[('customer', '=', 1)]")
    no_factura = fields.Char(string="No. de Factura", required=False, )
    no_quedan = fields.Char(string="No. de Quedan", required=False, )
    entrega = fields.Char(string="Entrega", required=False, )
    recibe = fields.Many2one('res.users', string='Recibe')











