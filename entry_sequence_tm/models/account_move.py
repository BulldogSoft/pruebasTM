# -*- encoding: utf-8 -*-

from odoo import models, fields, api

import datetime


class AccountMove(models.Model):
    _inherit = "account.move"

    entries_type = fields.Selection(
        string='Tipo Partida',
        selection=[
            ('D', 'Diarios'),
            ('A', 'Abono'),
            ('CA', 'Cargos'),
            ('CH', 'Cheques'),
            ('R', 'Remesas'),
            ('I', 'Ingresos'),
        ],
        required=False)

    entries_name = fields.Char(
        string='Secuencia',
        required=False)

    @api.model
    def create(self, values):
        res = super(AccountMove, self).create(values)
        # declaramos las variables
        year = datetime.date.today().strftime('%y')
        branch = self.env.context.get('user_id', self.env.user.branch_id.name)
        branch_name = ''.join([s[:1].upper() for s in branch.split(' ')])
        secuencia = None

        # buscamos la secuencia por tipo de entrada
        if res.entries_type == 'D':
            secuencia = self.env['ir.sequence'].next_by_code('sequence.diarios')
        if res.entries_type == 'I':
            secuencia = self.env['ir.sequence'].next_by_code('sequence.ingresos')
        if res.entries_type == 'R':
            secuencia = self.env['ir.sequence'].next_by_code('sequence.remesas')
        if res.entries_type in ['A', 'CA', 'CH']:
            secuencia = self.env['ir.sequence'].next_by_code('sequence.banco')

        # generamos la concatenacion
        for rec in res:
            if rec.entries_type in ['D', 'I']:
                tipo = rec.entries_type
                entries_name = "{}-{}{}{}".format(
                    tipo,
                    branch_name,
                    year,
                    secuencia,
                )
                res.entries_name = entries_name

            if rec.entries_type == 'R':
                tipo = 'BCO'
                entries_name = "{}-{}".format(
                    tipo,
                    secuencia,
                )
                res.entries_name = entries_name

            if rec.entries_type in ['A', 'CA', 'CH']:
                for journal in rec.journal_id:
                    bank = ''
                    number = ''
                    if journal:
                        if journal.bank_id:
                            bank_name = journal.bank_id.name
                            bank = ''.join([s[:1].upper() for s in bank_name.split(' ')])
                        if journal.bank_account_id:
                            bank_number = journal.bank_account_id.acc_number
                            number = bank_number[-3:]
                        bank_seq = bank + number
                        entries_name = "{}-{}".format(
                            bank_seq,
                            secuencia,
                        )
                        res.entries_name = entries_name
        return res

