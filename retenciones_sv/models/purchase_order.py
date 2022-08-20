# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange('order_line')
    def order_tax_update(self):
        for line in self.order_line:
            taxes = self.env['account.tax'].search([('name', '=', 'Percepción 1%')])
            fpos_name = self.fiscal_position_id.name
            posiciones = ['Gran Contribuyente']
            if fpos_name in posiciones and self.amount_untaxed >= 100:
                line.update({'taxes_id': [(4, taxes.id)]})
            if fpos_name in posiciones and self.amount_untaxed < 100:
                line.update({'taxes_id': [(3, taxes.id)]})
        return


class AccountInvoiceMove(models.Model):
    _inherit = "account.move"

    @api.onchange('invoice_line_ids', 'journal_id')
    def check_bill_lines(self):
        for invoice in self:
            taxes = self.env['account.tax'].search([('name', '=', 'Percepción 1%')])
            fpos_name = invoice.fiscal_position_id.name
            journal_name = invoice.journal_id.name
            diarios = ['Registro de Compras CCF', 'Notas de Crédito Compras']
            invoice_type = ['in_invoice', 'in_refund']
            posiciones = ['Gran Contribuyente']
            for rec in invoice.invoice_line_ids:
                if journal_name in diarios and invoice.move_type in invoice_type:
                    if fpos_name in posiciones:
                        if invoice.amount_untaxed >= 100:
                            rec.update({'tax_ids': [(4, taxes.id)]})

                        if invoice.amount_untaxed < 100:
                            rec.update({'tax_ids': [(3, taxes.id)]})

                        #funciones nuevas implementadas en la v14, estas hacen la actualizacion de los lines_ids
                        #actualizando la partida con las cantidades correspendientes cuando se ejecuta nuestro onchange
                        rec._onchange_price_subtotal()
                        rec._onchange_mark_recompute_taxes()

                if journal_name == 'Factura Consumidor Final Compras' and invoice.move_type in invoice_type:
                    if fpos_name in posiciones:
                        if invoice.amount_untaxed >= 100:
                            rec.update({'tax_ids': [(4, taxes.id)]})

                        if invoice.amount_untaxed < 100:
                            rec.update({'tax_ids': [(3, taxes.id)]})
                        rec._onchange_price_subtotal()
                        rec._onchange_mark_recompute_taxes()

            return super(AccountInvoiceMove, self)._onchange_invoice_line_ids()
