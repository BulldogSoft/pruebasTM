# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from lxml import etree


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_send_mail = fields.Boolean(config_parameter='discount.is_send_mail',string='Automatic Approval Notification Email.')
    salesuser_allowed_Discount = fields.Float(config_parameter='discount.salesuser_allowed_Discount', string="Sales Person Allowed Max.Discount(%)", default=0.0)
    salesmanager_allowed_Discount = fields.Float(config_parameter='discount.salesmanager_allowed_Discount', string="Sales Manager Allowed Max.Discount(%)", default=0.0)
    


class SaleOrder(models.Model):
    _inherit = "sale.order"  

    discount = fields.Float(string="Discount %",tracking=True)
    is_sales_manager = fields.Boolean(compute='_is_sales_manager',string='Is sales Manager')
    reject_reason = fields.Text(string='Reject Reason',tracking=True)
    is_reject_reason = fields.Boolean(string='Is Reject Reason')
    is_warning = fields.Boolean(compute='_is_warning_tick',string='Warning')
    is_discout_flow = fields.Boolean(string='Is Discount')
    is_discout_rejected = fields.Boolean(string='Discount Rejected')
    is_discout_approved = fields.Boolean(string='Discount Approved',tracking=True)
    discount_approver = fields.Many2one('res.users',compute='_discount_approver',string='Discount Approver',tracking=True)
    is_discout_hide = fields.Boolean(string='Hide',compute='_discount_hide',tracking=True)
  

    def _is_sales_manager(self):
        for order in self:
            if order.team_id and order.team_id.user_id:
                if self.env.user.id == order.team_id.user_id.id:
                    if self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
                        order.is_sales_manager = True
                    else:
                        order.is_sales_manager = False
                else:
                    order.is_sales_manager = False
            else:
                order.is_sales_manager = False

    def _discount_hide(self):
        for order in self:
            if order.is_sales_manager and order.is_discout_rejected:
                order.is_discout_hide = True
            else:
                order.is_discout_hide = False

    @api.depends('order_line.discount')
    def _is_warning_tick(self):
        for order in self:
            if self.env.user.has_group('sales_team.group_sale_salesman'):
                config_value = self.env['ir.config_parameter'].sudo().get_param('discount.salesuser_allowed_Discount')
            if self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
                config_value = self.env['ir.config_parameter'].sudo().get_param('discount.salesmanager_allowed_Discount')
            order.is_warning = False
            for line in order.order_line:
                if (line.discount > float(config_value) or order.is_discout_flow) and order.is_discout_approved == False:
                    order.is_warning = True
                    break

    def _discount_approver(self):
        for order in self:
            if order.team_id.user_id:
                order.discount_approver =  order.team_id.user_id.id
            else:
                order.discount_approver =  False


    def action_discount(self):
        context = dict(self._context or {})
        if not self.team_id:
            raise ValidationError('Warning! \n There Is No Sales Team, Kindly Map It.')
        if not self.discount_approver:
            raise ValidationError('Warning! \n There Is No Team Leader Mapped For This User Sales Team, Kindly Map It.')
        self.write(
            {
                'is_discout_flow': True,
                'discount':0.0,
                'is_discout_rejected': False,
                'is_discout_hide': False,
                'is_reject_reason': ''
            })

        config_value_mail = self.env['ir.config_parameter'].sudo().get_param('discount.is_send_mail')
        if config_value_mail:
            ir_model_data = self.env['ir.model.data']
            context.update({'email_cc': '','name':self.name,'partner_name':self.partner_id.name, 'email_to': self.discount_approver.partner_id.email,'email_subject': 'Discount Approval Mail'})
            template_id = ir_model_data.get_object_reference('discount', 'email_template_sale_approval')[1]
            try:
                self.env['mail.template'].browse(template_id).with_context(context).send_mail(self.id, force_send=True)
            except Exception:
                pass
        return True


    def apply_discount(self):
        config_value = self.env.user.has_group('product.group_discount_per_so_line')
        if not config_value:
            raise ValidationError('Warning! \n Kindly Enable Discount In Settings.')
        if not self.order_line:
            raise ValidationError('Warning! \n Kindly Select Atleast One Product.')
        for lines in self.order_line:
            if self.discount == 0.0:
                lines.write({'discount': self.discount})
            else:
                lines.write({'discount': self.discount})
        return True


    def action_approved(self):
        if self.is_sales_manager and self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
            config_value = self.env['ir.config_parameter'].sudo().get_param('discount.salesmanager_allowed_Discount')
        for order in self.order_line:
            print(order.discount)
            if order.discount > float(config_value):
                raise ValidationError('Warning! \n Cannot Approve, The Given Percentage Is Greater Than Your Allowed Discount.')
        self.is_discout_approved = True
        self.is_discout_flow = False
        self.is_warning = False
        return True

    def action_draft(self):
        self.is_discout_approved = False
        self.discount = 0.0
        return True


class sale_discout_reject(models.TransientModel):
    _name = "sale.discount.reject"

    reason = fields.Text(string='Reason',required=1)

    def action_apply(self):
        context = dict(self._context or {})
        sale_obj = self.env['sale.order']
        for sale_id in sale_obj.browse(context.get(('active_ids'), [])):
            if sale_id:
                sale_id.write(
                    {
                        'is_discout_flow': False,
                        'discount':0.0,
                        'state': 'draft',
                        'reject_reason': self.reason,
                        'is_discout_rejected': True,
                        'is_reject_reason': True
                    })
                config_value_mail = self.env['ir.config_parameter'].sudo().get_param('discount.is_send_mail')
                if config_value_mail:
                    ir_model_data = self.env['ir.model.data']
                    context.update({'email_cc': '','reject_reason':self.reason,'name':sale_id.name,'email_to': sale_id.user_id.partner_id.email,'email_subject': 'Approval Reject Mail'})
                    template_id = ir_model_data.get_object_reference('discount', 'email_template_sale_reject')[1]
                    try:
                        self.env['mail.template'].browse(template_id).with_context(context).send_mail(self.id, force_send=True)
                    except Exception:
                        pass
                return True
    

