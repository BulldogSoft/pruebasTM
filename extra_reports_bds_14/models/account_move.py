from odoo import fields, models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    concepto_factura = fields.Char(string="Concepto de Factura",  required=False, readonly=False)

    iva_calculo = fields.Float(string="IVA 13%",  required=False, compute='get_mercaderia_values')
    percepcion_calculo = fields.Float(string="Percepción 1%",  required=False, )
    form_aduanero = fields.Char(string="Formulario aduanero")
    fecha_ingreso = fields.Date(string="Fecha Ingreso")
    fecha_edicion = fields.Date(string="Fecha Edición")
    descuento_global = fields.Float(string="Descuento Global")

    def get_mercaderia_values(self):
        for bill in self:
            lineas = len(bill.invoice_line_ids)
            total_descuentos = []
            for line in bill.invoice_line_ids:
                total_descuentos.append(line.discount)
            descuentos = sum(total_descuentos)
            bill.descuento_global = descuentos / lineas
            print(bill.descuento_global)

            for taxes in bill.amount_by_group:
                iva_13 = 0
                if taxes[0] == 'IVA 13%':
                    iva_13 = taxes[1]
                    bill.iva_calculo = iva_13
                if taxes[0] == 'Percepción 1%':
                    percepcion_1 = taxes[1]
                    bill.percepcion_calculo = percepcion_1

    def print_mercaderia(self):
        return self.env.ref('extra_reports_bds_14.mercaderia_report').report_action(self)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    costo_sugerido = fields.Float(string="Costo Sugerido",  required=False, compute='compute_costo_sugerido')
    price_discount = fields.Float(string="Prec.desc")
    subtotal_line_discount = fields.Float(string="Subtotal con descuento")
    costo_sugerido_discount = fields.Float(string="Precio Sugerido con descuento")

    def compute_costo_sugerido(self):

        for line in self:
            costo_suge_percent = self.env['ir.config_parameter'].sudo().get_param('extra_report_bds_14.costo_sugerido')
            costo_suge = (float(costo_suge_percent) / 100) + 1
            line.costo_sugerido = costo_suge * line.price_unit
            ### descuentos
            discount = (line.discount / 100)
            price_unit_discount = line.price_unit * discount
            line.price_discount = line.price_unit - price_unit_discount
            costo_suge_discount = line.price_discount * costo_suge
            line.costo_sugerido_discount = costo_suge_discount
            line.subtotal_line_discount = line.price_discount * line.quantity



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    costo_sugerido = fields.Float("Porcentaje de costo sugerido")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
        costo_sugerido=params.get_param('extra_report_bds_14.costo_sugerido')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("extra_report_bds_14.costo_sugerido", self.costo_sugerido)

