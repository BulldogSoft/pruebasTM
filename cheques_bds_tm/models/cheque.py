
#################################################################################
import time
from odoo import api, models, fields
from dateutil.parser import parse
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .amount_to_text_sv import to_word
from odoo.exceptions import Warning

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    amount_text = fields.Char(string=('Amount to text'), store=True,
                              readonly=True,
                              compute='_amount_to_text',
                              track_visibility='onchange')

    cheque_concepto = fields.Char(string="En concepto de", required=False, )


    cheque_formato = fields.Selection(string="Formato de cheque", selection=[
                                                            ('agricola', 'Banco Agrícola'), ('bac', 'BAC Credomatic'),
                                                            ('proamerica','Banco Promerica'),('atlantida','Banco Atlántida'),
                                                            ('davivienda','Banco Davivienda'),('cuscatlan','Banco Cuscatlán')], required=False, )

    num_cheque = fields.Char(string="Numero de Cheque", required=False)
    cheque_date = fields.Date(string="Fecha de Cheque", required=False)
    is_cheque = fields.Boolean(string="Cheque",)
    autorizado_por = fields.Char(string="Autorizado por", required=False)
    recibido_por = fields.Char(string="Recibido por", required=False)


    @api.depends('amount')
    def _amount_to_text(self):
        for pay in self:
            pay.amount_text = to_word(pay.amount)

    @api.onchange('is_cheque')
    def compute_cheque_number(self):
        for cheque in self:
            if cheque.is_cheque == True:
                cheque.cheque_date = datetime.today()
                if cheque.journal_id.bank_account_id.secuencia:
                    codigo_sequence = cheque.journal_id.bank_account_id.secuencia.code
                    sequence = self.env['ir.sequence'].next_by_code(codigo_sequence)
                else:
                    sequence = ''
                cheque_correlativo = ''
                cheque_correlativo = str(sequence)
                cheque.num_cheque = cheque_correlativo
                print(cheque_correlativo)


class AccountMove(models.Model):
    _inherit = 'account.move'

    cheque_date = fields.Date(string="Fecha de Cheque", required=False)

    amount_text = fields.Char(string=('Amount to text'), store=True,
                              readonly=True,
                              compute='_amount_to_text',
                              track_visibility='onchange')

    cheque_concepto = fields.Char(string="En concepto de", required=False, )

    today = fields.Date(string="Today", default=datetime.today())

    cheque_formato = fields.Selection(string="Formato de cheque", selection=[
                                                            ('agricola', 'Banco Agrícola'), ('bac', 'BAC Credomatic'),
                                                            ('proamerica','Banco Promerica'),('atlantida','Banco Atlántida'),
                                                            ('davivienda','Banco Davivienda'),('cuscatlan','Banco Cuscatlán')], required=False, )

    partner_partidas_id = fields.Many2one('res.partner', string="Pago a", required=False,)

    num_cheque = fields.Char(string="Numero de Cheque", required=False, )
    is_cheque = fields.Boolean(string="Cheque",)
    autorizado_por = fields.Char(string="Autorizado por", required=False)
    recibido_por = fields.Char(string="Recibido por", required=False)


    @api.depends('amount_total')
    def _amount_to_text(self):
        for inv in self:
            inv.amount_text = to_word(inv.amount_total)


    def print_cheque(self):
        return self.env.ref('cheques_bds_tm.cheque_multi_formato_partidas_report').report_action(self)

    @api.onchange('is_cheque')
    def compute_cheque_number(self):
        for cheque in self:
            if cheque.is_cheque == True:
                cheque.cheque_date = datetime.today()
                if cheque.journal_id.bank_account_id.secuencia:
                    codigo_sequence = cheque.journal_id.bank_account_id.secuencia.code
                    sequence = self.env['ir.sequence'].next_by_code(codigo_sequence)
                else:
                    sequence = ''
                cheque_correlativo = ''
                cheque_correlativo = str(sequence)
                cheque.num_cheque = cheque_correlativo
                print(cheque_correlativo)

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    secuencia = fields.Many2one('ir.sequence',string="Secuencia Cheque")


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def cheque_date_default(self):
        cheque_date = datetime.today()
        return cheque_date

    cheque_concepto = fields.Char(string="En concepto de", required=False)

    cheque_formato = fields.Selection(string="Formato de cheque", selection=[
                                                            ('agricola', 'Banco Agrícola'), ('bac', 'BAC Credomatic'),
                                                            ('proamerica','Banco Promerica'),('atlantida','Banco Atlántida'),
                                                            ('davivienda','Banco Davivienda'),('cuscatlan','Banco Cuscatlán')], required=False, )

    num_cheque = fields.Char(string="Numero de Cheque", required=False)
    cheque_date = fields.Date(string="Fecha de Cheque", required=False)
    is_cheque = fields.Boolean(string="Cheque",)
    autorizado_por = fields.Char(string="Autorizado por", required=False)
    recibido_por = fields.Char(string="Recibido por", required=False)


    @api.onchange('is_cheque')
    def compute_cheque_number(self):
        for cheque in self:
            if cheque.is_cheque == True:
                cheque.cheque_date = datetime.today()
                if cheque.journal_id.bank_account_id.secuencia:
                    codigo_sequence = cheque.journal_id.bank_account_id.secuencia.code
                    sequence = self.env['ir.sequence'].next_by_code(codigo_sequence)
                else:
                    sequence = ''

                cheque_correlativo = ''
                cheque_correlativo = str(sequence)
                cheque.num_cheque = cheque_correlativo
                print(cheque_correlativo)



    def _create_payment_vals_from_wizard(self):
            payment_vals = {
                'date': self.payment_date,
                'amount': self.amount,
                'payment_type': self.payment_type,
                'partner_type': self.partner_type,
                'ref': self.communication,
                'journal_id': self.journal_id.id,
                'currency_id': self.currency_id.id,
                'partner_id': self.partner_id.id,
                'partner_bank_id': self.partner_bank_id.id,
                'payment_method_id': self.payment_method_id.id,
                'destination_account_id': self.line_ids[0].account_id.id,
                'is_cheque': self.is_cheque,
                'num_cheque': self.num_cheque,
                'cheque_date': self.cheque_date,
                'cheque_formato': self.cheque_formato,
                'cheque_concepto': self.cheque_concepto,
                'autorizado_por': self.autorizado_por,
                'recibido_por': self.recibido_por,
            }

            if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
                payment_vals['write_off_line_vals'] = {
                    'name': self.writeoff_label,
                    'amount': self.payment_difference,
                    'account_id': self.writeoff_account_id.id,
                }
            return payment_vals



