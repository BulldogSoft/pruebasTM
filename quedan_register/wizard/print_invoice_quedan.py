# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
import xlwt
import io
import base64
from xlwt import easyxf
import datetime

class PrintInvoiceSummary(models.TransientModel):
    _name = "print.invoice.quedan"
    
    @api.model
    def _get_from_date(self):
        company = self.env.user.company_id
        current_date = datetime.date.today()
        from_date = company.compute_fiscalyear_dates(current_date)['date_from']
        return from_date
    
    from_date = fields.Date(string='Desde', default=_get_from_date)
    to_date = fields.Date(string='Hasta', default=datetime.date.today())
    invoice_summary_file = fields.Binary('Reporte')
    file_name = fields.Char('Nombre')
    invoice_report_printed = fields.Boolean('Reporte realizado')
    invoice_status = fields.Selection([('all', 'Todas'), ('paid', 'Pagadas'), ('un_paid', 'Abiertas')],
                                      string='Estado de Facturas')
    
    
    
    def action_print_invoice_summary(self):
        new_from_date = self.from_date.strftime('%Y-%m-%d')
        new_to_date = self.to_date.strftime('%Y-%m-%d')

        workbook = xlwt.Workbook()
        column_heading_style = easyxf('font:height 200;font:bold True; align: horiz center;')
        worksheet = workbook.add_sheet('Quedan Emitidos')
        date_xf = easyxf(num_format_str='YYYY/MM/DD')
        body_style = easyxf('font:height 200; align: horiz center;')
        worksheet.write(2, 3, self.env.user.company_id.name, easyxf('font:height 200;font:bold True;align: horiz center;'))
        worksheet.write(4, 2, new_from_date, easyxf('font:height 200;font:bold True;align: horiz center;'))
        worksheet.write(4, 3, 'a',easyxf('font:height 200;font:bold True;align: horiz center;'))
        worksheet.write(4, 4, new_to_date,easyxf('font:height 200;font:bold True;align: horiz center;'))
        worksheet.write(6, 0, _('Quedan No.'), column_heading_style)
        worksheet.write(6, 1, _('Fecha'), column_heading_style)
        worksheet.write(6, 2, _('Proveedor'), column_heading_style)
        worksheet.write(6, 3, _('Recibe'), column_heading_style)
        worksheet.write(6, 4, _('Entrega'), column_heading_style)
        worksheet.write(6, 5, _('Factura No.'), column_heading_style)
        worksheet.write(6, 6, _('Referencia'), column_heading_style)
        worksheet.write(6, 7, _('Estado'), column_heading_style)
        worksheet.write(6, 8, _('Monto'), column_heading_style)

        worksheet.col(0).width = 4000
        worksheet.col(1).width = 4000
        worksheet.col(2).width = 8000
        worksheet.col(3).width = 8000
        worksheet.col(4).width = 8000
        worksheet.col(5).width = 4000
        worksheet.col(6).width = 4000
        worksheet.col(7).width = 4000
        worksheet.col(8).width = 4000
        row = 7

        for wizard in self:
            heading = 'Reporte de Quedan'
            worksheet.write_merge(0, 0, 0, 8, heading, easyxf('font:height 210; align: horiz center;pattern: pattern solid, fore_color black; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            quedan_objs = self.env['quedan.register.pro'].search([('fecha', '>=', wizard.from_date),
                                                                  ('fecha', '<=', wizard.to_date)])

            for quedan in quedan_objs:
                worksheet.write(row, 0, quedan.name, body_style)
                worksheet.write(row, 1, quedan.fecha, date_xf)
                worksheet.write(row, 2, quedan.partner_id.name, body_style)
                worksheet.write(row, 3, quedan.recibe, body_style)
                worksheet.write(row, 4, quedan.entrega.name, body_style)
                for invoice in quedan.invoice_ids:
                    worksheet.write(row, 5, invoice.invoice_id.number, body_style)
                    worksheet.write(row, 6, invoice.invoice_id.reference, body_style)
                    worksheet.write(row, 7, invoice.invoice_id.state, body_style)
                    worksheet.write(row, 8, invoice.invoice_id.amount_total, body_style)
                    row += 1

            fp = io.BytesIO()
            workbook.save(fp)
            excel_file = base64.encodestring(fp.getvalue())
            wizard.invoice_summary_file = excel_file
            wizard.file_name = 'Reporte de Quedan.xls'
            wizard.invoice_report_printed = True
            fp.close()
            return {
                    'view_mode': 'form',
                    'res_id': wizard.id,
                    'res_model': 'print.invoice.quedan',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self.env.context,
                    'target': 'new',
                       }
