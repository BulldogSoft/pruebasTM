# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api,fields,models,_

class AccountMove(models.Model):
    _inherit ='account.move'

    discount_porrateado = fields.Float(string="Descuento %", required=False, )

    def apply_discount_porrateado(self):

        for bill in self:
            for lines in bill.invoice_line_ids.with_context(check_move_validity=False):
                lines.discount = bill.discount_porrateado
                lines._onchange_mark_recompute_taxes()
                lines.compute_costo_sugerido()
            bill.with_context(check_move_validity=False)._recompute_dynamic_lines(recompute_all_taxes=True)


    # @api.onchange('invoice_line_ids')
    # def onchange_discount_porrateo(self):
    #     for bill in self:
    #         discount_list = []
    #         for lines in bill.invoice_line_ids:
    #             discount_list.append(lines.discount)
    #         #print(discount_list)
    #         new_discount_total = sum(discount_list)
    #         bill.discount_porrateado = new_discount_total

