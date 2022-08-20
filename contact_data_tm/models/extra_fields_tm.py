# copyright 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    n_resolucion = fields.Char(string='No. Resolución', required=False)
    n_serie = fields.Char(string='No. Serie', required=False)
    tipo_compra = fields.Selection(
        string='Tipo compra',
        selection=[('no_exenta', 'Compras de mercadería'),
                   ('exenta', 'Compras de mercaderías exenta'),
                   ('servicio', 'Servicios'),
                   ],
        required=False, )

    tipo_documento = fields.Selection(
        string='Tipo de documento',
        selection=[('ccf', 'Crédito Fiscal'),
                   ('fcf', 'Consumidor Final'),
                   ('fe', 'Factura Excluida'),
                   ('ticket', 'Recibo y Tickets'),
                   ],
        required=False, )

    tipo_documento_diarios = fields.Selection(
        string='Tipo de documento',
        selection=[('ccf', 'Crédito Fiscal'),
                   ('fcf', 'Consumidor Final'),
                   ],
        required=False, )

    @api.onchange('tipo_documento')
    def onchange_tipo_compra(self):
        ccf = self.env['account.journal'].search([('name', '=', 'Registro de Compras CCF')])
        fcf = self.env['account.journal'].search([('name', '=', 'Factura Consumidor Final Compras')])
        fe = self.env['account.journal'].search([('name', '=', 'Sujeto Excluido')])
        ticket = self.env['account.journal'].search([('name', '=', 'Recibo y Tickets')])
        if self.tipo_documento == 'ccf':
            self.journal_id = ccf.id
        if self.tipo_documento == 'fcf':
            self.journal_id = fcf.id
        if self.tipo_documento == 'fe':
            self.journal_id = fe.id
        if self.tipo_documento == 'ticket':
            self.journal_id = ticket.id

    @api.depends('move_type')
    def _compute_invoice_filter_type_domain(self):
        for move in self:
            if move.is_sale_document(include_receipts=True):
                move.invoice_filter_type_domain = 'sale'
            elif move.is_purchase_document(include_receipts=True):
                move.invoice_filter_type_domain = 'purchase'
            else:
                move.invoice_filter_type_domain = False

    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_ids(self):
        for m in self:
            if m.move_type == 'entry':
                company_id = m.company_id.id or self.env.company.id
                domain = [('company_id', '=', company_id),
                          ('type', 'in', ['sale', 'purchase', 'cash', 'bank', 'general'])]
                m.suitable_journal_ids = self.env['account.journal'].search(domain)
            else:
                journal_type = m.invoice_filter_type_domain or 'general'
                company_id = m.company_id.id or self.env.company.id
                domain = [('company_id', '=', company_id), ('type', '=', journal_type)]
                m.suitable_journal_ids = self.env['account.journal'].search(domain)

