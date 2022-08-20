# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    active = fields.Boolean(
        string='Libro Iva',
        help='- Estara activo si esta factura ya '
             'fue contabilizada en el libro de iva',
        default=True
    )

    reintegro = fields.Boolean(
        string='¿Es un reintegro?',
        help='Activar si la Factura es un reintegro',
        default=False)

    empresa_reintegro = fields.Many2one('res.partner',
                                        string='Proveedor')

    mostrar_libro_iva = fields.Boolean(
        string='Mostrar en Libros de IVA',
        required=False)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    impuesto = fields.Selection(
        string='Impuesto aplicado',
        selection=[('iva', 'IVA'),
                   ('percepcion', 'Percepción'),
                   ('renta', 'Renta'),
                   ('sub-total', 'Sub-Total'),
                   ('sub-total-ns', 'Sub-Total No sujetas'),
                   ],
        required=False, )

    linea_libro_iva = fields.Boolean(
        string='Mostrar en Libros de IVA',
        required=False)

