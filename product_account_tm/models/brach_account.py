# copyright 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from odoo.exceptions import UserError


class ResBranch(models.Model):
    _inherit = 'res.branch'


    #cuentas de producto
    product_expense_account = fields.Many2one(
        comodel_name='account.account',
        string='Gastos Producto',
        required=False)

    product_income_account = fields.Many2one(
        comodel_name='account.account',
        string='Ingresos Producto',
        required=False)

    #cuentas de impuesto ventas
    iva_ccf_account = fields.Many2one(
        comodel_name='account.account',
        string='IVA CCF',
        required=False)

    iva_fcf_account = fields.Many2one(
        comodel_name='account.account',
        string='IVA FCF',
        required=False)

    retencion_1_account = fields.Many2one(
        comodel_name='account.account',
        string='',
        required=False)

    exportacion_account = fields.Many2one(
        comodel_name='account.account',
        string='',
        required=False)


    # cuentas de impuesto compras
    iva_account_compras = fields.Many2one(
        comodel_name='account.account',
        string='IVA Compras',
        required=False)

    fovial_account_compras = fields.Many2one(
        comodel_name='account.account',
        string='Fovial',
        required=False)

    percepcion_account_compras = fields.Many2one(
        comodel_name='account.account',
        string='Percepción 1%',
        required=False)

    renta_account_compras = fields.Many2one(
        comodel_name='account.account',
        string='Renta 10%',
        required=False)

    cotrans_account_compras = fields.Many2one(
        comodel_name='account.account',
        string='Cotrans',
        required=False)

    importaciones_13_account_compras = fields.Many2one(
        comodel_name='account.account',
        string='Importaciones 13%',
        required=False)


class AccountMove(models.Model):
    _inherit = "account.move"

    cuentas_asignadas = fields.Boolean(
        string='Cuentas_asignadas',
        required=False)

    def bill_account_assignment(self):
        branch = self.env.context.get('user_id', self.env.user.branch_id)
        for rec in self.line_ids:
            for il in self.invoice_line_ids:
                if il.tax_ids:
                    for tax in il.tax_ids:
                        if rec.branch_id == branch:
                            self.cuentas_asignadas = True
                            if self.move_type == 'in_invoice':
                                if tax.name == 'IVA 13%':
                                    if rec.name == 'IVA 13%':
                                        rec.account_id = branch.iva_account_compras
                                if tax.name == 'Fovial':
                                    if rec.name == 'Fovial':
                                        rec.account_id = branch.fovial_account_compras
                                if tax.name == 'Percepción 1%':
                                    if rec.name == 'Percepción 1%':
                                        rec.account_id = branch.percepcion_account_compras
                                if tax.name == 'Renta 10%':
                                    if rec.name == 'Renta 10%':
                                        rec.account_id = branch.renta_account_compras
                                if tax.name == 'Cotrans':
                                    if rec.name == 'Cotrans':
                                        rec.account_id = branch.cotrans_account_compras
                                if tax.name == 'Importaciones 13%':
                                    if rec.name == 'Importaciones 13%':
                                        rec.account_id = branch.renta_account_compras

                            else:
                                raise UserError(('La sucursal en la que estas (Sucursal: %s) no coincide con la sucursal de '
                                                 'la factura (Sucursal: %s), verifica estar en la sucursal correcta para '
                                                 'asignar cuentas') % (branch.name, self.branch_id.name))

                else:
                    self.cuentas_asignadas = True

    def button_draft(self):
        super(AccountMove, self).button_draft()
        self.cuentas_asignadas = False




