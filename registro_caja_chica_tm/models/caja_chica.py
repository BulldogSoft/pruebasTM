# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from odoo.exceptions import UserError
from odoo import fields, models, api, _


class CajaChicaModel(models.Model):
    _name = "caja.chica"

    name = fields.Char(string='N°', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('cancel', 'Cancelado'),
        ('draft', 'Borrador'),
        ('open', 'En Proceso'),
        ('done', 'Hecho')], 'State', default='draft',
        copy=False, readonly=True, track_visibility='onchange')
    company_id = fields.Many2one('res.company', string=_('Compañia'),
                                 change_default=True,
                                 default=lambda self: self.env.user.company_id.id)
    partner_id = fields.Many2one('res.partner', string='Proveedor', domain="[('is_vendor', '=', 1)]")
    fecha = fields.Date(string="Fecha", required=False,  default=date.today())
    concepto = fields.Char(
        string='Concepto',
        required=False)
    total = fields.Float(
        string='Total',
        required=False)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('caja.chica.seq') or _('New')
        result = super(CajaChicaModel, self).create(vals)
        return result

    def button_validate(self):
        for rec in self:
            rec.write({'state': 'open'})

    def button_done(self):
        for rec in self:
            rec.write({'state': 'done'})

    def button_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancel'})












