# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, exceptions


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def print_report_se(self):
        return self.env.ref('l10n_invoice_reports_sv.report_se_tm').report_action(self)

