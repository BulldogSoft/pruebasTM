# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo.exceptions import UserError
from odoo import fields, models, api, _


class QuedanRegisterPro(models.Model):
    _name = "quedan.register.pro"

    name = fields.Char(string='Quedan No', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string=_('Compañia'),
                                 change_default=True,
                                 default=lambda self: self.env.user.company_id.id)

    branch_id = fields.Many2one('res.branch', string=_('Sucursal'),
                                change_default=True,
                                default=lambda self: self.env.user.branch_id.id)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('open', 'En Proceso'),
        ('done', 'Validado')], 'State', default='draft',
        copy=False, readonly=True, track_visibility='onchange')
    fecha = fields.Date(string="Fecha", required=False,  default=date.today())
    fecha_vencimiento = fields.Date(string="Fecha Vencimiento", required=False, default=date.today())
    partner_id = fields.Many2one('res.partner', string='Proveedor', domain="[('is_vendor', '=', 1)]")
    recibe = fields.Char(string="Recibe", required=False, )
    entrega = fields.Many2one('res.users', string='Entrega')
    invoice_ids = fields.One2many('quedan.invoice',
                                  'quedan_id', string='Facturas')
    amount_total = fields.Float('Total', compute='_compute_total_amount', digits=0,
                                store=True, track_visibility='always')
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term',
                                      readonly=True, states={'draft': [('readonly', False)]})

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('quedan.register') or _('New')
        result = super(QuedanRegisterPro, self).create(vals)
        return result

    @api.depends('invoice_ids.total')
    def _compute_total_amount(self):
        self.amount_total = sum(line.total for line in self.invoice_ids)

    def button_validate(self):
        for rec in self:
            for line in rec.invoice_ids:
                if rec.partner_id.name != line.proveedor:
                    raise UserError(
                        _("El quedan y Facturas deben ser del mismo Proveedor"))
            rec.write({'state': 'open'})

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        company_id = self.company_id.id
        p = self.partner_id if not company_id else self.partner_id.with_context(force_company=company_id)
        if p:
            self.payment_term_id = p.property_supplier_payment_term_id.id


class QuedanInvoice(models.Model):
    _name = 'quedan.invoice'
    _description = 'Facturas'

    quedan_id = fields.Many2one('quedan.register.pro')
    invoice_id = fields.Many2one('account.move', 'Factura', required=False,
                                 domain=[('move_type', '=', 'in_invoice'), ('state', 'in', ['posted'])])
    factura = fields.Char(
        string='Factura',
        required=False)
    proveedor = fields.Char(string='Proveedor', required=False)
    reference = fields.Char(string='Referencia', required=True)
    total = fields.Float(string='Total', required=True)

    # @api.onchange('invoice_id')
    # def onchange_product_id(self):
    #     for rec in self:
    #         self.invoice_id = rec.invoice_id.id
    #         self.proveedor = rec.invoice_id.partner_id.name or ''
    #         self.reference = rec.invoice_id.ref or ''
    #         self.total = rec.invoice_id.amount_total or 0.0











