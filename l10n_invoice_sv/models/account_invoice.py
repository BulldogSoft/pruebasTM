# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, exceptions


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    refund_method_bds = fields.Selection(selection=[
            ('refund', 'Partial Refund'),
            ('cancel', 'Full Refund'),
            ('modify', 'Full refund and new draft invoice')
        ], string='Credit Method',)

    state_refund = fields.Selection([
        ('refund', 'Anulada'),
        ('no_refund', 'Valida'),
    ], string="Anulación", index=True, readonly=True, default='no_refund',
        track_visibility='onchange', copy=False, compute='anu_document')

    @api.depends('reversal_move_id', 'refund_method_bds')
    def anu_document(self):
        for rec in self:
            if not rec.reversal_move_id:
                rec.state_refund = 'no_refund'
            if rec.reversal_move_id or rec.reversal_move_id.refund_method_bds == 'refund':
                rec.state_refund = 'no_refund'
            if rec.reversal_move_id and rec.reversal_move_id.refund_method_bds == 'cancel' \
                    or rec.reversal_move_id.refund_method_bds == 'modify':
                rec.state_refund = 'refund'

    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        self.ensure_one()
        self.sent = True

        report = self.journal_id.type_report

        if report == 'ccf':
            return self.env.ref(
                'l10n_invoice_sv.report_credito_fiscal').report_action(self)
        if report == 'fcf':
            return self.env.ref('l10n_invoice_sv.report_consumidor_final').report_action(self)
        if report == 'exp':
            return self.env.ref(
                'l10n_invoice_sv.report_exportacion').report_action(self)
        if report == 'ndc':
            return self.env.ref('l10n_invoice_sv.report_ndc').report_action(
                self)
        if report == 'anu':
            return self.env.ref(
                'account.account_invoice_action_report_duplicate').\
                report_action(self)
        if report == 'axp':
            return self.env.ref(
                'l10n_invoice_sv.report_anul_export').report_action(self)

    def msg_error(self, campo):
        raise exceptions.ValidationError(
            "No puede emitir un documento si falta "
            "un campo Legal Verifique {}".format(campo))

    def action_invoice_open(self):
        """
        validamos que partner cumple los requisitos basados en el tipo
        de documento de la sequencia del diario selecionado
        :return: Native super method
        """
        inv_type = self.type
        # si es factura normal
        type_report = self.journal_id.type_report

        if type_report == 'ccf':
            if not self.partner_id.parent_id:
                if not self.partner_id.nrc:
                    self.msg_error("N.R.C.")
                if not self.partner_id.nit:
                    self.msg_error("N.I.T.")
                if not self.partner_id.giro:
                    self.msg_error("Giro")

        if type_report == 'fcf':
            if not self.partner_id.parent_id:
                if not self.partner_id.nit:
                    self.msg_error("N.I.T.")
                if self.partner_id.company_type == 'person':
                    if not self.partner_id.dui:
                        self.msg_error("D.U.I.")


        # si es retificativa
        if type_report == 'ndc':
            if not self.partner_id.parent_id:
                if not self.partner_id.nrc:
                    self.msg_error("N.R.C.")
                if not self.partner_id.nit:
                    self.msg_error("N.I.T.")
                if not self.partner_id.giro:
                    self.msg_error("Giro")

        return super(AccountInvoice, self).action_invoice_open()

    def print_report(self):
        return self.env.ref('l10n_invoice_sv.report_invoice_quedan').report_action(self)

    def print_report_se(self):
        return self.env.ref('l10n_invoice_sv.report_sujeto_excluido').report_action(self)

