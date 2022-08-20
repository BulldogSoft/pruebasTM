# copyright 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    nota_tm = fields.Char(
        string='Nota',
        required=False)

    purchase_journal = fields.Many2one('account.journal', 'Documento')

    tipo_documento = fields.Selection(
        string='Tipo de documento',
        selection=[('ccf', 'Crédito Fiscal'),
                   ('fcf', 'Consumidor Final'),
                   ('fe', 'Factura Excluida'),
                   ('ticket', 'Recibo y Tickets'),
                   ],
        required=False, )

    @api.onchange('tipo_documento')
    def onchange_journal_po(self):
        ccf = self.env['account.journal'].search([('name', '=', 'Registro de Compras CCF')])
        fcf = self.env['account.journal'].search([('name', '=', 'Factura Consumidor Final Compras')])
        fe = self.env['account.journal'].search([('name', '=', 'Sujeto Excluido')])
        ticket = self.env['account.journal'].search([('name', '=', 'Recibo y Tickets')])
        if self.tipo_documento == 'ccf':
            self.purchase_journal = ccf.id
        if self.tipo_documento == 'fcf':
            self.purchase_journal = fcf.id
        if self.tipo_documento == 'fe':
            self.purchase_journal = fe.id
        if self.tipo_documento == 'ticket':
            self.purchase_journal = ticket.id

    def _prepare_invoice(self):
        """Prepare the dict of values to create the new invoice for a purchase order.
        """
        self.ensure_one()
        move_type = self._context.get('default_move_type', 'in_invoice')
        journal = self.env['account.move'].with_context(default_move_type=move_type)._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting purchase journal for the company %s (%s).') % (
            self.company_id.name, self.company_id.id))

        partner_invoice_id = self.partner_id.address_get(['invoice'])['invoice']
        invoice_vals = {
            'ref': self.partner_ref or '',
            'move_type': move_type,
            'narration': self.notes,
            'currency_id': self.currency_id.id,
            'invoice_user_id': self.user_id and self.user_id.id or self.env.user.id,
            'partner_id': partner_invoice_id,
            'fiscal_position_id': (
                        self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(partner_invoice_id)).id,
            'payment_reference': self.partner_ref or '',
            'partner_bank_id': self.partner_id.bank_ids[:1].id,
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
            'tipo_documento': self.tipo_documento,
            'journal_id': self.purchase_journal.id,
            'nota_tm': self.nota_tm,
        }
        return invoice_vals

