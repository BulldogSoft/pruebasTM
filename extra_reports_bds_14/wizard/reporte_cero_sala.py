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


class ReporteCeroSala(models.TransientModel):
    _name = "reporte.cero.sala"

    sucursal = fields.Many2one('res.branch', string="Sucursal", required=False)


    reporte_cero_file = fields.Binary('Reporte')
    file_name = fields.Char('Nombre')
    reporte_cero_printed = fields.Boolean('Reporte realizado')

    def generar_reporte_cero(self):

        workbook = xlwt.Workbook()
        column_heading_style = easyxf('font:height 200;font:bold True; align: horiz center;')
        background_gray = easyxf(
            'font:height 230; align: horiz center;pattern: pattern solid, fore_color gray50; font: color white; font:bold True;' "borders: top thin,bottom thin")
        worksheet = workbook.add_sheet('Reporte Cero en Sala')
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

        worksheet.write(2, 0, 'Sucursal', background_gray)
        worksheet.write(2, 1, self.sucursal.name, center)

        # worksheet.write(4, 1, new_from_date, easyxf('font:height 200;font:bold True;align: horiz center;'))
        # worksheet.write(4, 2, 'a', easyxf('font:height 200;font:bold True;align: horiz center;'))
        # worksheet.write(4, 3, new_to_date, easyxf('font:height 200;font:bold True;align: horiz center;'))

        worksheet.write(6, 0, _('NB'), left_b)
        worksheet.write(6, 1, _('Nombre'), left_b)
        worksheet.write(6, 2, _('Descripción'), left_b)
        worksheet.write(6, 3, _('Cantidad en Sala'), left_b)
        worksheet.write(6, 4, _('Cantidad en Bodega'), left_b)
        worksheet.write(6, 5, _('Ultima Actualización'), left_b)
        worksheet.write(6, 6, _('Ultimo Movimiento'), left_b)
        worksheet.write(6, 7, _('Bodega'), left_b)

        worksheet.col(0).width = 4000
        worksheet.col(1).width = 6000
        worksheet.col(2).width = 6000
        worksheet.col(3).width = 6000
        worksheet.col(4).width = 6000
        worksheet.col(5).width = 6000
        worksheet.col(6).width = 6000
        worksheet.col(7).width = 6000

        row = 7

        for wizard in self:
            heading = 'Reporte cero en Sala'
            worksheet.write_merge(0, 0, 0, 7, heading, easyxf(
                'font:height 230; align: horiz center;pattern: pattern solid, fore_color gray50; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            #vars
            sucursal_id = wizard.sucursal
            #search
            productos = self.env['product.product'].search([])
            ubicaciones = self.env['stock.location'].search([('branch_id', '=', sucursal_id.id)])
            sala = self.env['stock.location'].search([('branch_id', '=', sucursal_id.id),('name','ilike','sala')],limit=1)
            bodega = self.env['stock.location'].search([('branch_id', '=', sucursal_id.id),('name','ilike', 'bodega')])
            #loops
            for bod in bodega:
                for producto in productos:
                    if sala not in producto.stock_quant_ids.location_id:
                        if bod in producto.stock_quant_ids.location_id:
                            for quant in producto.stock_quant_ids:
                                if bod.name in quant.location_id.name:
                                    last_move = self.env['stock.move.line'].search([('product_id','=',quant.product_id.id)],order='date DESC',limit=1)
                                    #print(last_move.date)
                                    last_date = fields.Datetime.context_timestamp(self, last_move.date).strftime(
                                        '%d-%m-%Y, %H:%M:%S')
                                    today = datetime.now()
                                    worksheet.write(row, 0, quant.product_id.default_code, left)
                                    worksheet.write(row, 1, quant.product_id.name, left)
                                    worksheet.write(row, 2, quant.product_id.product_type.name, left)
                                    worksheet.write(row, 3, '0', left)
                                    worksheet.write(row, 4, quant.available_quantity, left)
                                    if last_move.date.day == today.day and last_move.date.month == today.month and last_move.date.year == today.year:
                                        worksheet.write(row, 5, 'HOY', left)
                                    else:
                                        worksheet.write(row, 5, last_date, left)

                                    if last_move.move_id.picking_type_id.code == 'incoming':
                                        worksheet.write(row, 6, 'COMPRA', left)
                                    if last_move.move_id.picking_type_id.code == 'outgoing':
                                        worksheet.write(row, 6, 'VENTA', left)
                                    if last_move.move_id.picking_type_id.code == 'internal':
                                        worksheet.write(row, 6, 'TRANSLADO', left)
                                    worksheet.write(row, 7, quant.location_id.name, left)
                                    row+=1


            fp = io.BytesIO()
            workbook.save(fp)
            excel_file = base64.encodestring(fp.getvalue())
            wizard.reporte_cero_file = excel_file
            wizard.file_name = 'Reporte cero en sala.xls'
            wizard.reporte_cero_printed = True
            fp.close()
            return {
              #  'error': error,
                'view_mode': 'form',
                'res_id': wizard.id,
                'res_model': 'reporte.cero.sala',
                'type': 'ir.actions.act_window',
                'context': self.env.context,
                'target': 'new',
            }