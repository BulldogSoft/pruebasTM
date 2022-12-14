# -*- coding: utf-8 -*-
from odoo import models

class PrintJournalEntries(models.Model):
    _inherit = 'account.move'

    def print_journal_entries(self):
        return self.env.ref('print_partidas_contables.action_journal_entries_report').report_action(self)
