from odoo import models, fields, api, _
import xlwt
import io
import base64
from xlwt import easyxf
import datetime
import time
from datetime import time, date, datetime
from odoo.exceptions import Warning
import pytz
from pytz import timezone


class ReporteCeroTienda(models.TransientModel):
    _name = "reporte.cero.tienda"

    bodega_no_tiene = fields.Many2one('stock.location', string="No tiene", required=False, domain=[('usage', '=', 'internal')])

    bodega_si_tiene = fields.Many2one('stock.location', string="Si tiene", required=False, domain=[('usage', '=', 'internal')])

    reporte_cero_file = fields.Binary('Reporte')
    file_name = fields.Char('Nombre')
    reporte_cero_printed = fields.Boolean('Reporte realizado')

    def generar_reporte_cero(self):

        workbook = xlwt.Workbook()
        column_heading_style = easyxf('font:height 200;font:bold True; align: horiz center;')
        background_gray = easyxf(
            'font:height 230; align: horiz center;pattern: pattern solid, fore_color gray50; font: color white; font:bold True;' "borders: top thin,bottom thin")
        worksheet = workbook.add_sheet('Reporte Cero en Tienda')
        date_xf = easyxf(num_format_str='DD/MM/YYYY')
        hour_xf = easyxf(num_format_str='HH:MM')
        float_xf = easyxf(num_format_str='0.00')
        body_style = easyxf('font:height 200; align: horiz center;')
        left = easyxf('font:height 200; align: horiz left;')
        left_b = easyxf('font:height 200; align: horiz left; font:bold True;')
        right = easyxf('font:height 200; align: horiz right;')
        right_b = easyxf('font:height 200; align: horiz right; font:bold True;')
        center = easyxf('font:height 200; align: horiz center;')
        center_b = easyxf('font:height 200; align: horiz center; font:bold True;')

        worksheet.write(2, 0, 'No tiene', background_gray)
        worksheet.write(2, 1, self.bodega_no_tiene.name, center)
        worksheet.write(3, 0, 'Si tiene', background_gray)
        worksheet.write(3, 1, self.bodega_si_tiene.name, center)

        # worksheet.write(4, 1, new_from_date, easyxf('font:height 200;font:bold True;align: horiz center;'))
        # worksheet.write(4, 2, 'a', easyxf('font:height 200;font:bold True;align: horiz center;'))
        # worksheet.write(4, 3, new_to_date, easyxf('font:height 200;font:bold True;align: horiz center;'))

        worksheet.write(6, 0, _('NB'), left_b)
        worksheet.write(6, 1, _('Nombre'), left_b)
        worksheet.write(6, 2, _('Existencias'), left_b)
        worksheet.write(6, 3, _('Sucursal'), left_b)

        worksheet.col(0).width = 4000
        worksheet.col(1).width = 6000
        worksheet.col(2).width = 6000
        worksheet.col(3).width = 6000

        row = 7

        for wizard in self:
            heading = 'Reporte cero en Tienda'
            worksheet.write_merge(0, 0, 0, 3, heading, easyxf(
                'font:height 230; align: horiz center;pattern: pattern solid, fore_color gray50; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            #vars
            sucursal = wizard.bodega_no_tiene.branch_id
            bodega_no = wizard.bodega_no_tiene
            bodega_si = wizard.bodega_si_tiene
            #search
            productos = self.env['product.product'].search([])

            for product in productos:
                if bodega_no not in product.stock_quant_ids.location_id:
                    if bodega_si in product.stock_quant_ids.location_id:
                        for quant in product.stock_quant_ids:
                            if quant.location_id.id == bodega_si.id:
                                print(quant.product_id.name)
                                worksheet.write(row, 0, quant.product_id.default_code, left)
                                worksheet.write(row, 1, quant.product_id.name, left)
                                worksheet.write(row, 2, quant.available_quantity, left)
                                worksheet.write(row, 3, quant.location_id.name, left)
                                row += 1

            fp = io.BytesIO()
            workbook.save(fp)
            excel_file = base64.encodestring(fp.getvalue())
            wizard.reporte_cero_file = excel_file
            wizard.file_name = 'Reporte cero en tienda.xls'
            wizard.reporte_cero_printed = True
            fp.close()
            return {
               #'error': error,
                'view_mode': 'form',
                'res_id': wizard.id,
                'res_model': 'reporte.cero.tienda',
                'type': 'ir.actions.act_window',
                'context': self.env.context,
                'target': 'new',
            }