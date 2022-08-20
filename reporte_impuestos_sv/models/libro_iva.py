# -*- coding: utf-8 -*-
import time
import calendar
from datetime import date, datetime
from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from . import func


class LibroIva(models.Model):
    _name = 'libro.iva'
    _inherit = ['mail.thread', 'mail.activity.mixin',
                'portal.mixin']  # ## Redes Sociales
    _description = "Libros de Iva"
    _order = 'fecha, mes'

    # campos del encabezado
    name = fields.Char('Nombre', copy=False, default='Reporte',
                       track_visibility='always')

    fecha = fields.Date(string=_('Fecha'),
                        index=True, help=_("Fecha de realizado el informe"),
                        copy=False, default=time.strftime('%Y-%m-%d'),
                        track_visibility='onchange')

    company_id = fields.Many2one('res.company', string=_('Compañia'),
                                 change_default=True,
                                 default=lambda
                                     self: self.env.user.company_id.id)

    branch_id = fields.Many2one(
        'res.branch', string='Sucursal',
        change_default=True,
        default=lambda self: self.env.user.branch_id.id)

    company_currency_id = fields.Many2one('res.currency',
                                          related='company_id.currency_id',
                                          string="Company Currency",
                                          readonly=True)

    nrc = fields.Char(string=_("NRC"), readonly=True,
                      help=_("Numero de registro contribuyente"),
                      default=lambda self: self.env.user.company_id.nrc)

    nit = fields.Char(string=_("NIT"), readonly=True,
                      help=_("Numero de Identificacion Tributario"),
                      default=lambda self: self.env.user.company_id.nit)

    mes = fields.Selection([
        ('01', 'Enero'),
        ('02', 'Febrero'),
        ('03', 'Marzo'),
        ('04', 'Abril'),
        ('05', 'Mayo'),
        ('06', 'Junio'),
        ('07', 'Julio'),
        ('08', 'Agosto'),
        ('09', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre'),
    ], string=_("Mes"), index=True, default=time.strftime("%m"), copy=False,
        required=True, track_visibility='onchange')

    state = fields.Selection([
        ('draft', _('Borrador')),
        ('open', _('Validado')),
        ('cancel', _('Cancelado')),
    ], string=_('Estado'), index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=_(
            " * El Borrador sirve para verificar la "
            "informacion correspondiente.\n"
            " * El Validado sirve para dar por realizado el libro de iva.\n"
            " * El cancelado se hace cuando ha fallado un libro."))

    responsable_id = fields.Many2one(
        'res.users', _('Responsable'),
        required=False, readonly=True,
        states={'draft': [('readonly', False)]},
        help=_(
            "Seleccione la persona que validara el libro"),
        track_visibility='always')

    usuario_id = fields.Many2one('res.users', string=_('Usuario'),
                                 readonly=True,
                                 default=lambda self: self.env.user)

    type = fields.Selection(
        [('fcf', 'Libro Consumidor Final'), ('ccf', 'Libro Credito Fiscal'),
         ('compras', 'Libro Compras'), ('renta', 'Reporte de Renta')], string=None,
        default=lambda self: self._context.get('type', 'fcf'), )

    # campos que contienen el detalle y resumen del reporte.

    libro_line_compras = fields.One2many('libro.line', 'libro_iva_id',
                                         'Lineas Libro', readonly=True)
    libro_line_ccf = fields.One2many('libro.line', 'libro_iva_id',
                                     'Lineas Libro', readonly=True)
    libro_line_fcf = fields.One2many('libro.line', 'libro_iva_id',
                                     'Lineas Libro', readonly=True)
    resumen_line_fcf = fields.One2many('resumen.line', 'libro_iva_id',
                                       'Lineas Resumen', readonly=True)
    resumen_line_ccf = fields.One2many('resumen.line', 'libro_iva_id',
                                       'Lineas Resumen', readonly=True)
    resumen_line_compras = fields.One2many('resumen.line', 'libro_iva_id',
                                           'Lineas Resumen', readonly=True)

    ################    RENTAAAAAAAAAAAAAA #####################
    libro_line_renta = fields.One2many('libro.line', 'libro_iva_id',
                                       'Lineas Libro', readonly=True)

    resumen_line_renta = fields.One2many('resumen.line', 'libro_iva_id',
                                         'Lineas Resumen', readonly=True)

    ##################################################
    def iva_print(self):
        if self.type == 'fcf':
            return self.env.ref(
                'reporte_impuestos_sv.libro_iva_fcf').report_action(self)
        if self.type == 'ccf':
            return self.env.ref(
                'reporte_impuestos_sv.libro_iva_ccf').report_action(self)
        if self.type == 'compras':
            return self.env.ref(
                'reporte_impuestos_sv.libro_iva_compras').report_action(self)

        if self.type == 'renta':
            return self.env.ref('reporte_impuestos_sv.libro_iva_compras_renta').report_action(self)

    # funciones para obtener valores
    @api.model
    def create(self, vals):

        meses = {
            '01': 'Enero',
            '02': 'Febrero',
            '03': 'Marzo',
            '04': 'Abril',
            '05': 'Mayo',
            '06': 'Junio',
            '07': 'Julio',
            '08': 'Agosto',
            '09': 'Septiembre',
            '10': 'Octubre',
            '11': 'Noviembre',
            '12': 'Diciembre'
        }
        inv_type = {
            'fcf': 'Consumidor Final',
            'ccf': 'Credito Fiscal',
            'compras': 'Compras',
            'renta': 'Reporte de Renta'
        }
        mes_actual = meses.get(time.strftime("%m"))
        name = "{} - {} - {}".format(
            inv_type.get(vals.get('type')), str(date.today().year), mes_actual)
        vals.update({'name': name})
        libro_id = super(LibroIva, self).create(vals)
        return libro_id

    def datos_iva_compra(self):
        # Limpiamos registros por cada actualizacion
        func.limpieza(self)
        # Variables Iniciales Requeridas
        branch_id = self.branch_id.id
        company_id = self.company_id.id
        invoice_obj = self.env['account.move']
        correlativo = 1
        mes = int(self.mes)
        year = self.fecha.year
        dia = calendar.monthrange(year, mes)
        refund_list = []

        for i in range(dia[1]):
            # aumentamos uno a la variable que representa los dias
            i += 1
            fecha_contable = date(year, mes, i)

            # buscamos todas las facturas del dia
            invoice_list = invoice_obj.search([
                ('date', '=', fecha_contable),
                ('branch_id', '=', branch_id),
                ('state', 'in', ['posted']),
                ('move_type', 'in', ['in_invoice', 'entry']),
                ('journal_id.type_report', '=', 'compras')],
                order='date')

            for inv_id in invoice_list:
                credito_fiscal = 0
                cg_internas = 0
                cg_importacion = 0
                ce_internas = 0
                ce_importacion = 0
                cns_internas = 0
                cns_importacion = 0
                percepcion = 0
                retencion = 0
                excluidas = 0
                renta = 0
                totales = 0

                name = inv_id.empresa_reintegro.name or inv_id.partner_id.name
                nrc = inv_id.partner_id.nrc
                numero = inv_id.ref or inv_id.dcl_documento
                dui = inv_id.partner_id.dui
                nit = inv_id.partner_id.nit
                fecha = inv_id.invoice_date or inv_id.date

                if inv_id.state_refund == 'no_refund' or inv_id.move_type == 'entry' and inv_id.mostrar_libro_iva:
                    for tax_id in inv_id.line_ids:
                        if tax_id.name == 'Intrusivo':
                            ce_importacion = tax_id.debit

                        if tax_id.name == 'Combustibles':
                            ce_internas = tax_id.debit

                        if tax_id.name == 'Importación 0%':
                            ce_importacion = inv_id.amount_untaxed

                        if tax_id.name == 'Renta 10%':
                            cns_internas = inv_id.amount_untaxed
                            renta = tax_id.debit

                        if tax_id.name == 'IVA 13%':
                            credito_fiscal = tax_id.debit
                            cg_internas = inv_id.amount_untaxed

                        if tax_id.name == 'Importación 13%':
                            credito_fiscal = tax_id.debit
                            cg_importacion = inv_id.amount_untaxed

                        if tax_id.name == 'Percepción 1%':
                            percepcion = tax_id.debit

                        # condiciones para partidas contables
                        if tax_id.linea_libro_iva and tax_id.impuesto == 'sub-total' or tax_id.impuesto == 'sub-total-ns':
                            name = tax_id.partner_id.name
                            nrc = tax_id.partner_id.nrc

                        if tax_id.linea_libro_iva and tax_id.impuesto == 'sub-total':
                            cg_internas += tax_id.debit or tax_id.credit

                        if tax_id.linea_libro_iva and tax_id.impuesto == 'iva':
                            credito_fiscal = tax_id.debit or tax_id.credit

                        if tax_id.linea_libro_iva and tax_id.impuesto == 'percepcion':
                            percepcion += tax_id.debit or tax_id.credit

                        if tax_id.linea_libro_iva and tax_id.impuesto == 'sub-total-ns':
                            cg_internas += tax_id.debit or tax_id.credit

                        if tax_id.linea_libro_iva and tax_id.impuesto == 'renta':
                            renta += tax_id.debit or tax_id.credit

                        totales = credito_fiscal + cg_internas + cg_importacion + ce_internas + ce_importacion + \
                                  cns_internas + cns_importacion + retencion + excluidas + renta

                    self.env['libro.line'].create({
                        'libro_iva_id': self.id,
                        'correlativo': correlativo,
                        'fecha_doc': fecha,
                        'fecha_con': fecha_contable,
                        'num_doc': numero,
                        'nrc': nrc,
                        'dui': dui,
                        'nit': nit,
                        'name': name,
                        'internas_e': ce_internas,
                        'importaciones_e': ce_importacion,
                        'internas_g': cg_internas,
                        'internas_ns': cns_internas,
                        'importacion_ns': cns_importacion,
                        'importaciones_g': cg_importacion,
                        'iva_credito_g': credito_fiscal,
                        'retenciones': retencion,
                        'percepcion': percepcion,
                        'totales': totales,
                        'excluidas': renta,
                    })
                else:
                    refund_list.append(inv_id.reversal_move_id.id)
                    self.env['libro.line'].create({
                        'libro_iva_id': self.id,
                        'correlativo': correlativo,
                        'fecha_doc': fecha,
                        'fecha_con': fecha_contable,
                        'num_doc': numero,
                        'nrc': nrc,
                        'dui': dui,
                        'nit': nit,
                        'name': name,
                        'internas_e': 0,
                        'importaciones_e': 0,
                        'internas_g': 0,
                        'internas_ns': 0,
                        'importacion_ns': 0,
                        'importaciones_g': 0,
                        'iva_credito_g': 0,
                        'retenciones': 0,
                        'percepcion': 0,
                        'totales': 0,
                        'excluidas': 0,
                    })

        self.resumen_compras()
        return True

    ##################################################
    def resumen_compras(self):
        # Inicio de variables

        internas_e = 0
        importaciones_e = 0
        internas_g = 0
        importaciones_g = 0
        internas_ns = 0
        importacion_ns = 0
        iva_credito_g = 0
        retenciones = 0
        percepciones = 0
        excluidas = 0
        totales = 0

        # recorremos todas las lineas para obtener datos
        for l in self.libro_line_compras:
            internas_e += l.internas_e
            importaciones_e += l.importaciones_e
            internas_g += l.internas_g
            importaciones_g += l.importaciones_g
            internas_ns += l.internas_ns
            importacion_ns += l.importacion_ns
            iva_credito_g += l.iva_credito_g
            retenciones += l.retenciones
            percepciones += l.percepcion
            excluidas += l.excluidas
            totales += l.totales

        # guardamos todos los resumen
        self.env['resumen.line'].create({
            'detalle': "Compras Internas Exentas",
            'total': internas_e,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Importaciones Exentas",
            'total': importaciones_e,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Compras Internas Gravadas",
            'total': internas_g,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Importaciones Gravadas",
            'total': importaciones_g,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Credito Fiscal",
            'total': iva_credito_g,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Retenciones",
            'total': retenciones,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Percepciones",
            'total': percepciones,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Ventas Totales",
            'total': totales,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Internas No Sujetas",
            'total': internas_ns,
            'libro_iva_id': self.id,
        })

        self.env['resumen.line'].create({
            'detalle': "Importacion No Sujetas",
            'total': importacion_ns,
            'libro_iva_id': self.id,
        })

        self.env['resumen.line'].create({
            'detalle': "Renta",
            'total': excluidas,
            'libro_iva_id': self.id,
        })

    ##################################################

    def datos_iva_ccf(self):
        # Limpiamos registros por cada actualizacion
        func.limpieza(self)
        # Variables Iniciales Requeridas
        company_id = self.company_id.id
        invoice_obj = self.env['account.move']
        correlativo = 1
        mes = int(self.mes)
        year = self.fecha.year
        dia = calendar.monthrange(year, mes)
        refund_list = []

        for i in range(dia[1]):
            # variables iniciales requeridas por dia
            # aumentamos uno a la variable que representa los dias
            i += 1
            fecha = date(year, mes, i)

            # buscamos todas las facturas del dia
            invoice_list = invoice_obj.search([
                ('invoice_date', '=', fecha),
                ('company_id', '=', company_id),
                ('state', 'in', ['posted']),
                ('move_type', 'in', ['out_invoice', 'out_refund']),
                ('journal_id.type_report', '=', 'ccf')],
                order='name, invoice_date')

            for inv_id in invoice_list:
                debito_fiscal = 0
                ventas_gravadas = 0
                ventas_exentas = 0
                retenciones = 0
                totales = inv_id.amount_total
                # metodos si es factura no retificada
                numeracion = func.numeracion(inv_id.name)

                # #print numeracion,'Datos'
                prefijo = numeracion.get('pre')
                longitud = numeracion.get('longitud')
                numero = inv_id.ref_retencion or int(numeracion.get('num'))
                name = inv_id.partner_id.name
                nrc = inv_id.partner_id.nrc
                doc_refund = inv_id.reversal_move_id.ref

                if inv_id.state_refund == 'no_refund':
                    for tax_id in inv_id.line_ids:
                        if tax_id.name == 'IVA 13% Ventas':
                            debito_fiscal = tax_id.credit
                            ventas_gravadas += inv_id.amount_untaxed
                            # #print debito_fiscal,ventas_gravadas,'IVA'
                        if tax_id.name == 'Retención 1%':
                            retenciones = tax_id.credit

                    # #print debito_fiscal,ventas_gravadas,'IVA'
                    self.env['libro.line'].create({
                        'libro_iva_id': self.id,
                        'correlativo': correlativo,
                        'fecha_doc': fecha,
                        'num_doc': numero,
                        'prefijo': prefijo,
                        'name': name,
                        'nrc': nrc,
                        'exentas_nosujetas': ventas_exentas,
                        'gravadas': ventas_gravadas,
                        'retenciones': retenciones,
                        'debito_fiscal': debito_fiscal,
                        'totales': totales,
                    })
                else:
                    if datetime.strftime(inv_id.reversal_move_id.invoice_date, '%Y-%m-%d'):
                        refund_list.append(inv_id.reversal_move_id.id)
                        self.env['libro.line'].create({
                            'libro_iva_id': self.id,
                            'correlativo': correlativo,
                            'fecha_doc': fecha,
                            'num_doc': numero,
                            'prefijo': doc_refund,
                            'name': name,
                            'nrc': nrc,
                            'exentas_nosujetas': 0,
                            'gravadas': 0,
                            'retenciones': 0,
                            'debito_fiscal': 0,
                            'totales': 0,
                        })

        self.resumen_ccf()
        return True

    def resumen_ccf(self):
        # Inicio de variables
        ventas_exentas = 0
        ventas_gravadas = 0
        retenciones = 0
        debito_fiscal = 0
        totales = 0

        # recorremos todas las lineas para obtener datos
        for l in self.libro_line_ccf:
            ventas_exentas += l.exentas_nosujetas
            ventas_gravadas += l.gravadas
            retenciones += l.retenciones
            debito_fiscal += l.debito_fiscal
            totales += l.totales
            # #print ventas_exentas, ventas_gravadas,
            # exportaciones, retenciones, debito_fiscal, totales

        # guardamos todos los resumen
        self.env['resumen.line'].create({
            'detalle': "Ventas Exentas",
            'total': ventas_exentas,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Ventas Gravadas",
            'total': ventas_gravadas,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Debito Fiscal",
            'total': debito_fiscal,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Retenciones",
            'total': retenciones,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Ventas Totales",
            'total': totales,
            'libro_iva_id': self.id,
        })

    # #################################################
    def datos_iva_fcf(self):
        # limpiamos registros por cada actualizacion
        func.limpieza(self)
        # Variables Iniciales Requeridas
        branch_id = self.branch_id.id
        company_id = self.company_id.id
        invoice_obj = self.env['account.move']
        h = 0
        mes = int(self.mes)
        # #print self.fecha
        year = self.fecha.year
        # #print year
        dia = calendar.monthrange(year, mes)
        refund_list = []
        for i in range(dia[1]):
            # variables iniciales requeridas por dia
            num_inicial = 0
            ventas_exentas = 0
            ventas_gravadas = 0
            exportaciones = 0
            nosujetas = 0
            ventas_totales = 0
            debito_fiscal = 0

            # aumentamos uno a la variable que representa los dias
            i += 1

            fecha = date(year, mes, i)
            ##print fecha
            # buscamos todas las facturas del dia

            invoice_list = invoice_obj.search([
                ('invoice_date', '=', fecha),
                ('branch_id', '=', branch_id),
                ('state', 'in', ['posted']),
                ('move_type', '=', 'out_invoice'),
                ('journal_id.type_report', 'in', ['fcf', 'exp'])],
                order='name, invoice_date')
            # #print invoice_list,'LISTADO DE FACTURAS'
            # revisamos toda las facturas del dia
            prefijo_ant = 0
            numero_ant = 0
            for inv_id in invoice_list:

                # validamos que no esta retificada
                if inv_id.state_refund == 'no_refund':
                    # metodos si es factura no retificada
                    numeracion = func.numeracion(inv_id.name)

                    # #print numeracion,'Datos'
                    prefijo = numeracion.get('pre')
                    longitud = numeracion.get('longitud')
                    numero = int(numeracion.get('num'))
                    # #print numero,'Numero'
                    # #print num_inicial, 'Incial'
                    # #print numero_ant, 'Num Anterior'

                    if num_inicial == 0:
                        num_inicial = inv_id.name
                        num_anterior = numero
                        prefijo_ant = prefijo

                    else:

                        if prefijo_ant != prefijo or (
                                num_anterior) != numero:
                            # Guardar
                            self.env['libro.line'].create({
                                'libro_iva_id': self.id,
                                'dia': i,
                                'num_inicial': num_inicial,
                                'exentas_nosujetas': ventas_exentas,
                                'gravadas': ventas_gravadas,
                                'exportaciones': exportaciones,
                                'nosujetas': nosujetas,
                                'totales': ventas_totales,
                                'debito_fiscal': debito_fiscal,
                            })
                            num_anterior = numero
                            num_inicial = inv_id.name
                            ventas_exentas = 0
                            ventas_gravadas = 0
                            exportaciones = 0
                            retenciones = 0
                            ventas_totales = 0
                            debito_fiscal = 0
                            prefijo_ant = prefijo
                            h = 0  # Datos Guardados
                        else:
                            if prefijo_ant == prefijo:
                                prefijo_ant = prefijo
                            if (num_anterior + 1) == numero:
                                num_anterior = numero

                    # Generamos datos a guardarse
                    for tax_id in inv_id.line_ids:
                        # #print tax_id.tax_id.name
                        # #print tax_id.tax_id.type_tax
                        # ventas normales
                        if tax_id.name == 'IVA 13% Ventas':
                            ventas_gravadas += tax_id.credit + inv_id.amount_untaxed
                            ventas_totales += tax_id.credit + inv_id.amount_untaxed
                            debito_fiscal += inv_id.amount_total
                        if inv_id.invoice_line_ids.tax_ids.name == 'Exportaciones 0%':
                            exportaciones = inv_id.amount_untaxed
                            ventas_totales = inv_id.amount_untaxed
                        if tax_id.name == 'Exentas 0%':
                            ventas_exentas += tax_id.credit + inv_id.amount_untaxed
                            ventas_totales += tax_id.credit + inv_id.amount_untaxed
                        if tax_id.name == 'No sujetas 0%':
                            nosujetas += tax_id.credit + inv_id.amount_untaxed
                            ventas_totales += tax_id.credit + inv_id.amount_untaxed

                    h = 1  # establecemos que hay valors sin guardarse

                else:
                    # validamos que la anulacion sea del mes correspondiente
                    if datetime.strftime(inv_id.reversal_move_id.invoice_date, '%Y-%m-%d'):
                        refund_list.append(inv_id.reversal_move_id.id)
                        # debemos guardar los datos buenos
                        # creamos un salto guardamos los datos
                        # de la retificativa
                        # metodos si es factura retificada

                        if h == 1:
                            # #print 'Guardar Datos Buenos'
                            self.env['libro.line'].create({
                                'libro_iva_id': self.id,
                                'dia': i,
                                'num_inicial': num_inicial,
                                'exentas_nosujetas': ventas_exentas,
                                'gravadas': ventas_gravadas,
                                'exportaciones': exportaciones,
                                'nosujetas': nosujetas,
                                'totales': ventas_totales,
                                'debito_fiscal': debito_fiscal,
                            })
                            h = 0  # Datos Guardados

                        num_inicial = inv_id.name
                        ventas_exentas = 0
                        ventas_gravadas = 0
                        exportaciones = 0
                        nosujetas = 0
                        ventas_totales = 0
                        debito_fiscal = 0

                        self.env['libro.line'].create({
                            'libro_iva_id': self.id,
                            'dia': i,
                            'num_inicial': num_inicial,
                            'exentas_nosujetas': ventas_exentas,
                            'gravadas': ventas_gravadas,
                            'exportaciones': exportaciones,
                            'nosujetas': nosujetas,
                            'totales': ventas_totales,
                            'debito_fiscal': debito_fiscal,
                        })
                        h = 0  # Datos Guardados

                        num_inicial = 0

                        ##print 'RETIFICADA'

            # validamos que no existan datos sin guardar al salir
            if h == 1:
                h = 0  # Datos Guardados
                self.env['libro.line'].create({
                    'libro_iva_id': self.id,
                    'dia': i,
                    'num_inicial': num_inicial,
                    'exentas_nosujetas': ventas_exentas,
                    'gravadas': ventas_gravadas,
                    'exportaciones': exportaciones,
                    'nosujetas': nosujetas,
                    'totales': ventas_totales,
                    'debito_fiscal': debito_fiscal,
                })
                ventas_exentas = 0
                ventas_gravadas = 0
                exportaciones = 0
                nosujetas = 0
                ventas_totales = 0
                debito_fiscal = 0

            # Buscamos Facturas Anuladas de mes anteriores
            # print(refund_list)
            refund_old = self.env['account.move'].search([
                ('id', 'not in', refund_list),
                ('state', 'in', ['posted']),
                ('invoice_date', '=', fecha),
                ('move_type', '=', "out_refund"),
                ('journal_id.type_report', 'in', ['anu', 'ndc']),
                ('reversal_move_id.journal_id.type_report', '=', 'fcf')])

            for r_id in refund_old:
                for tax_id in r_id.tax_line_ids:
                    # #print tax_id.tax_id.name
                    # #print tax_id.tax_id.type_tax
                    # ventas normales
                    if tax_id.tax_id.type_tax == 'tax2':
                        debito_fiscal += tax_id.amount
                        ventas_gravadas += tax_id.base + tax_id.amount
                    if tax_id.tax_id.type_tax == 'exento':
                        ventas_exentas += tax_id.base + tax_id.amount
                    if tax_id.tax_id.type_tax == 'tax6':
                        retenciones += abs(tax_id.amount)
                    if tax_id.tax_id.type_tax == 'tax4':
                        exportaciones += tax_id.base
                    ventas_totales = ventas_gravadas + ventas_exentas + exportaciones

                self.env['libro.line'].create({
                    'libro_iva_id': self.id,
                    'dia': i,
                    'num_inicial': r_id.reversal_move_id.name,
                    'exentas_nosujetas': ventas_exentas * -1,
                    'gravadas': ventas_gravadas * -1,
                    'exportaciones': exportaciones * -1,
                    'nosujetas': nosujetas * -1,
                    'totales': ventas_totales * -1,
                    'debito_fiscal': debito_fiscal * -1,
                })
                num_inicial = inv_id.name
                ventas_exentas = 0
                ventas_gravadas = 0
                exportaciones = 0
                nosujetas = 0
                ventas_totales = 0
                debito_fiscal = 0

        self.resumen_fcf()

    def resumen_fcf(self):
        # Inicio de variables
        ventas_exentas = 0
        ventas_gravadas = 0
        exportaciones = 0
        nosujetas = 0
        debito_fiscal = 0
        totales = 0

        # recorremos todas las lineas para obtener datos
        for l in self.libro_line_fcf:
            ventas_exentas += l.exentas_nosujetas
            ventas_gravadas += l.gravadas
            exportaciones += l.exportaciones
            nosujetas += l.nosujetas
            debito_fiscal += l.debito_fiscal
            totales = ventas_exentas + ventas_gravadas + exportaciones
            # #print ventas_exentas, ventas_gravadas, exportaciones,
            # retenciones, debito_fiscal, totales

        # guardamos todos los resumen
        self.env['resumen.line'].create({
            'detalle': "Ventas Exentas",
            'total': ventas_exentas,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Ventas Gravadas",
            'total': ventas_gravadas,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Exportaciones",
            'total': exportaciones,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Debito Fiscal",
            'total': debito_fiscal,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "Ventas Totales",
            'total': totales,
            'libro_iva_id': self.id,
        })
        self.env['resumen.line'].create({
            'detalle': "No Sujetas",
            'total': nosujetas,
            'libro_iva_id': self.id,
        })

    ###########################################################################

    def datos_iva_renta(self):
        # Limpiamos registros por cada actualizacion
        func.limpieza(self)
        # Variables Iniciales Requeridas
        company_id = self.company_id.id
        invoice_obj = self.env['account.move']
        correlativo = 1
        mes = int(self.mes)
        year = self.fecha.year
        dia = calendar.monthrange(year, mes)
        refund_list = []

        for i in range(dia[1]):
            # aumentamos uno a la variable que representa los dias
            i += 1
            fecha = date(year, mes, i)

            # buscamos todas las facturas del dia
            invoice_list = invoice_obj.search([
                ('date', '=', fecha),
                ('company_id', '=', company_id),
                ('state', 'in', ['posted']),
                ('move_type', '=', 'in_invoice'),
                ('journal_id.type_report', '=', 'compras')],
                order='name, date')

            for inv_id in invoice_list:
                renta = 0
                totales = inv_id.amount_untaxed

                name = inv_id.empresa_reintegro.name or inv_id.partner_id.name
                nrc = inv_id.partner_id.nrc
                nit = inv_id.partner_id.nit
                dui = inv_id.partner_id.dui
                numero = inv_id.ref

                if inv_id.state_refund == 'no_refund':
                    for tax_id in inv_id.tax_line_ids:
                        if tax_id.name == 'Renta 10%':
                            cns_internas = inv_id.amount_untaxed
                            renta = tax_id.debit

                    # #print totales,'TOTALES'
                    self.env['libro.line'].create({
                        'libro_iva_id': self.id,
                        'correlativo': correlativo,
                        'fecha_doc': fecha,
                        'num_doc': numero,
                        'nrc': nrc,
                        'dui': dui,
                        'nit': nit,
                        'name': name,
                        'totales': totales,
                        'excluidas': renta,
                    })
                else:
                    refund_list.append(inv_id.reversal_move_id.id)
                    self.env['libro.line'].create({
                        'libro_iva_id': self.id,
                        'correlativo': correlativo,
                        'fecha_doc': fecha,
                        'num_doc': numero,
                        'nrc': nrc,
                        'dui': dui,
                        'nit': nit,
                        'name': name,
                        'totales': totales,
                        'excluidas': renta,
                    })
                # aumentamos el correlativo de cantidad de facturas
                correlativo += 1

            tax_ids = self.env['account.tax'].search([
                ('company_id', '=', company_id),
                ('type_tax_use', '=', 'none'),
                # ('tax_adjustment', '=', True)
            ])
            for tax in tax_ids:

                move_list = self.env['account.move.line'].search([
                    ('tax_line_id', '=', tax.id),
                    ('account_id', '=', tax.account_id.id),
                    ('company_id', '=', company_id),
                    ('date', '=', fecha)])
                ##print move_list
                for m in move_list:
                    iva = m.balance if tax.type_tax == 'iva_compra' else 0
                    retencion = m.balance if tax.type_tax == 'retencion' else 0
                    percepcion = m.balance if tax.type_tax == 'percepcion1' or \
                                              tax.type_tax == 'percepcion2' \
                        else 0
                    self.env['libro.line'].create({
                        'libro_iva_id': self.id,
                        'correlativo': correlativo,
                        'fecha_doc': fecha,
                        'num_doc': m.name,
                        'nrc': m.partner_id.nrc,
                        'name': m.partner_id.name,
                        'totales': iva + retencion + percepcion,
                        'excluidas': m.balance if tax.type_tax == 'exento' else 0,
                    })
                    correlativo += 1
        self.resumen_renta()
        return True

    ##################################################
    def resumen_renta(self):
        # Inicio de variables

        excluidas = 0
        totales = 0

        # recorremos todas las lineas para obtener datos
        for l in self.libro_line_renta:
            excluidas += l.excluidas
            totales += l.totales
            # # print ventas_exentas, ventas_gravadas, exportaciones,
            # retenciones, debito_fiscal, totales

        # guardamos todos los resumen
        self.env['resumen.line'].create({
            'detalle': "Ventas Totales",
            'total': totales,
            'libro_iva_id': self.id,
        })

        self.env['resumen.line'].create({
            'detalle': "Renta",
            'total': excluidas,
            'libro_iva_id': self.id,
        })
