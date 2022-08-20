from itertools import groupby
from datetime import datetime, timedelta
import pytz
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
from odoo.tools import html2plaintext
import odoo.addons.decimal_precision as dp


class PosDocumentType(models.Model):
	_inherit = 'pos.config'

	doctype_id = fields.Many2many('pos.doc.type',string='Tipos de documento')
	secuencia_ticket = fields.Many2one('ir.sequence', string="Secuencia de Ticket")
	secuencia_fcf = fields.Many2one('ir.sequence', string="Secuencia de FCF")
	secuencia_ccf = fields.Many2one('ir.sequence', string="Secuencia de CCF")



class PosOrderDocType(models.Model):
	_inherit = 'pos.order'

	doctype_id = fields.Many2one('pos.doc.type', string="Tipo de Documento")
	order_secuencia = fields.Char(string="Secuencia", required=False)

	@api.model
	def _order_fields(self, ui_order):
		result = super(PosOrderDocType, self)._order_fields(ui_order)
		#get pos.config for generate secuence
		caja = self.env['pos.session'].search([('id','=',ui_order['pos_session_id'])],limit=1)
		#get doctype
		documento = self.env['pos.doc.type'].search([('id', '=', ui_order['doctype_id'])],limit=1)
		#generate secuence
		if documento.code == 'FCF':
			secuencia_code = caja.config_id.secuencia_fcf.code
		if documento.code == 'TCK':
			secuencia_code = caja.config_id.secuencia_ticket.code
		if documento.code == 'CCF':
			secuencia_code = caja.config_id.secuencia_ccf.code

		secuencia = self.env['ir.sequence'].next_by_code(secuencia_code)
		result['order_secuencia'] = secuencia

		if 'doctype_id' in ui_order.keys():
			result['doctype_id'] = ui_order['doctype_id']
		return result



	@api.model
	def _process_order(self, order, draft, existing_order):
		if 'doctype_id' in order.keys():
			order['data']['doctype_id'] = order['doctype_id']
		new = super(PosOrderDocType,self)._process_order(order, draft, existing_order)
		return new