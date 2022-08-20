# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Res_Partner(models.Model):
	_inherit = 'res.partner'
	_description = "Contact"
	
	is_customer = fields.Boolean(string="Es Cliente")
	is_vendor = fields.Boolean(string="Es Proveedor")


