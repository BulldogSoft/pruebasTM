    # -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from odoo import fields, models, api, tools, _


class retaceoPoliza(models.Model):

    _name = 'retaceo.poliza'
    _description = 'Retaceo El Salvador'


    #poliza
    name = fields.Char(string="No", required=False, readonly=True)
    order_id = fields.Many2one('purchase.order', string='Numero PO', domain=[('state', 'in', ['purchase', 'done'])])
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('progress', 'En Proceso'),
        ('done', 'Validado')], 'State', default='draft',
        copy=False, readonly=True, track_visibility='onchange')

    journal_id = fields.Many2one('account.journal', string='Diario', required=True,
                                 states={'progress': [('readonly', True)]})

    move_id = fields.Many2one(
        'account.move', 'Partida',
        copy=False, readonly=True)

    descripcion = fields.Char(string="Descripción", required=False, )
    guia_bl = fields.Char(string="Guia/BL", required=False, )
    metodo_division = fields.Selection(string='Metodo de Reparto',
                                       selection=[('precio', 'Precio'),
                                                  ('cantidad', 'Cantidad'),
                                                  ('volumen', 'Volumen'),
                                                  ('peso', 'Peso'), ],
                                       required=False, )

    fecha = fields.Date(string="Fecha", required=True)
    tipo_importacion = fields.Selection(string='Tipo de importación',
                                        selection=[('maritimo', 'Maritimo'),
                                                   ('aereo', 'Aéreo'),
                                                   ('terrestre', 'Terrestre')
                                                   ],
                                        required=False, )
    incoterm_id = fields.Many2one('account.incoterms', string='Incoterm')
    fecha_zarpe = fields.Date(string="Fecha de Zarpe", required=False, )
    fecha_entrada = fields.Date(string="Fecha entrada en Aduana", required=False, )
    aduanas = fields.Selection(string='Aduana Entrada',
                               selection=[('1', '1'),
                                          ('2', '2'),
                                          ('3', '3'),
                                          ('4', '4'), ],
                               required=False, )
    company_id = fields.Many2one('res.company', string='Compañía')
    cost_lines = fields.One2many('retaceo.internacion', 'cost_id', 'Gastos')
    valuation_adjustment_lines = fields.One2many('retaceo.linea', 'cost_id', 'Ajustes de Valorización',)
    gastos_nacionales = fields.One2many('retaceo.nacionales',
                                        'gastos_line', string='Order Lines')

    total_gastos = fields.Float("Total", compute='_compute_total_gastos', compute_sudo=True,
                                  store=True, )
    amount_total = fields.Float(
        'Total', compute='_compute_total_amount',
        digits=0, store=True, track_visibility='always')

    total_former_cost = fields.Float(string="Total FOB", compute='_compute_total_former_cost', compute_sudo=True,
                                     store=True)
    total_porrateo_int = fields.Float(string="Total PGI", compute='_compute_total_porrateo_int', compute_sudo=True,
                                      store=True, )
    total_vicf = fields.Float(string="Total V.CIF", compute='_compute_total_vcif', compute_sudo=True,
                                      store=True, )

    avg_landed_cost_lines = fields.One2many('average.landed.cost.lines',
                                            'line_id', string='Order Lines')

    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    @api.depends('cost_lines.total')
    def _compute_total_amount(self):
        self.amount_total = sum(line.total for line in self.cost_lines)

    @api.depends('gastos_nacionales.total')
    def _compute_total_gastos(self):
        self.total_gastos = sum(line.total for line in self.gastos_nacionales)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('poliza.code')
        return super(retaceoPoliza, self).create(vals)

    def button_progress(self):
        if any(cost.state != 'draft' for cost in self):
            raise UserError(
                _(''))
        return self.write({'state': 'progress'})

    def button_validate(self):
        for cost in self:
            for line in cost.avg_landed_cost_lines.filtered(lambda line: line.product_id):
                if line.product_id.qty_available != 00.0:
                    line.product_id.sudo().standard_price = ((line.product_id.standard_price *
                                                             line.product_id.qty_available) +
                                                             (line.quantity * line.average_landed_cost)) /\
                                                            (line.quantity + line.product_id.qty_available)
                else:
                    line.product_id.sudo().standard_price = line.average_landed_cost
                line.action_entry()
            cost.write({'state': 'done'})

    def get_valuation_lines(self):
        self.ensure_one()
        lines = []
        for move in self._get_targeted_order_ids():
            # it doesn't make sense to make a landed cost for a product that isn't set as being valuated in real time at real cost
            vals = {
                'product_id': move.product_id.id,
                'quantity': move.product_qty,
                'unit_price': move.price_unit,
                'former_cost': move.price_subtotal,
                'weight': move.product_id.weight * move.product_qty,
                'volume': move.product_id.volume * move.product_qty
            }
            lines.append(vals)

        if not lines and self.mapped('order_id'):
            raise UserError(_("You cannot apply landed costs on the chosen transfer(s). Landed costs can only be applied for products with automated inventory valuation and FIFO costing method."))
        return lines

    def compute_landed_cost(self):
        AdjustementLines = self.env['retaceo.linea']
        AdjustementLines.search([('cost_id', 'in', self.ids)]).unlink()

        towrite_dict = {}
        for cost in self.filtered(lambda cost: cost.order_id):
            rounding = cost.currency_id.rounding
            total_qty = 0.0
            total_cost = 0.0
            total_weight = 0.0
            total_price = 0.0
            total_volume = 0.0
            total_line = 0.0
            all_val_line_values = cost.get_valuation_lines()
            for val_line_values in all_val_line_values:
                for cost_line in cost.cost_lines:
                    val_line_values.update({'cost_id': cost.id, 'cost_line_id': cost_line.id})
                    self.env['retaceo.linea'].create(val_line_values)
                total_qty += val_line_values.get('quantity', 0.0)
                total_weight += val_line_values.get('weight', 0.0)
                total_volume += val_line_values.get('volume', 0.0)
                total_price += val_line_values.get('unit_price', 0.0)

                former_cost = val_line_values.get('former_cost', 0.0)
                # round this because former_cost on the valuation lines is also rounded
                total_cost += former_cost

                total_line += 1

            for line in cost.cost_lines:
                value_split = 0.0
                for valuation in cost.valuation_adjustment_lines:
                    value = 0.0
                    if valuation.cost_line_id and valuation.cost_line_id.id == line.id:
                        if self.metodo_division == 'cantidad' and total_qty:
                            per_unit = (line.total / total_qty)
                            value = valuation.quantity * per_unit
                        elif self.metodo_division == 'peso' and total_weight:
                            per_unit = (line.total / total_weight)
                            value = valuation.weight * per_unit
                        elif self.metodo_division == 'volumen' and total_volume:
                            per_unit = (line.total / total_volume)
                            value = valuation.volume * per_unit
                        elif self.metodo_division == 'equal':
                            value = (line.total / total_line)
                        elif self.metodo_division == 'precio' and total_cost:
                            per_unit = (line.total / total_cost)
                            value = valuation.former_cost * per_unit
                        else:
                            value = (line.total / total_line)

                        if rounding:
                            value = tools.float_round(value, precision_rounding=rounding, rounding_method='UP')
                            fnc = min if line.total > 0 else max
                            value = fnc(value, line.total - value_split)
                            value_split += value

                        if valuation.id not in towrite_dict:
                            towrite_dict[valuation.id] = value
                        else:
                            towrite_dict[valuation.id] += value
        for key, value in towrite_dict.items():
            AdjustementLines.browse(key).write({'additional_landed_cost': value})
        return True

    def _get_targeted_order_ids(self):
        return self.order_id.order_line

    def compute_average_landed_cost(self):
        AverageLandedCostLines = self.env['average.landed.cost.lines']
        AverageLandedCostLines.search([('line_id', 'in', self.ids)]).unlink()
        for line in self.valuation_adjustment_lines:
            data = self.avg_landed_cost_lines.filtered(lambda t: t.line_id.id == line.cost_id.id)
            if not data:
                self.avg_landed_cost_lines.create({
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'average_landed_cost': line.costo_unitario,
                    'total_costo': line.costo_total,
                    'line_id': self.id,
                })
            else:
                val = self.avg_landed_cost_lines.filtered(
                    lambda t: t.line_id.id == line.cost_id.id and t.product_id.id == line.product_id.id)
                if val:
                    val.average_landed_cost = line.costo_unitario
                else:
                    self.avg_landed_cost_lines.create({
                        'product_id': line.product_id.id,
                        'quantity': line.quantity,
                        'average_landed_cost': line.costo_unitario,
                        'total_costo': line.costo_total,
                        'line_id': self.id
                    })

    @api.depends('valuation_adjustment_lines.porrateo_int')
    def _compute_total_porrateo_int(self):
        for gastos in self:
            gastos.total_porrateo_int = round(sum(gastos.valuation_adjustment_lines.mapped('porrateo_int')), 2)

    @api.depends('valuation_adjustment_lines.former_cost')
    def _compute_total_former_cost(self):
        for gastos in self:
            gastos.total_former_cost = round(sum(gastos.valuation_adjustment_lines.mapped('former_cost')), 2)

    @api.depends('valuation_adjustment_lines.vcif')
    def _compute_total_vcif(self):
        for gastos in self:
            gastos.total_vicf = round(sum(gastos.valuation_adjustment_lines.mapped('vcif')), 2)


class Internacion(models.Model):

    _name = 'retaceo.internacion'
    _description = 'Costos'

    cost_id = fields.Many2one(
        'retaceo.poliza', 'Landed Cost',
        required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Producto')
    invoice_id = fields.Many2one('account.move', 'Factura', required=True,
                                 domain=[('move_type', '=', 'in_invoice'), ('state', '=', 'posted')])
    reference = fields.Char(string='Referencia', required=False)
    total = fields.Float(string='Total', required=False)

    @api.onchange('invoice_id')
    def onchange_product_id(self):
        self.reference = self.invoice_id.ref or ''
        self.total = self.invoice_id.amount_untaxed or 0.0


class LineaPorrateo(models.Model):
    _name = 'retaceo.linea'
    _description = 'Linea Porrateo'

    name = fields.Char(
        'Description',
        store=True)
    cost_id = fields.Many2one(
        'retaceo.poliza', 'Landed Cost',
        ondelete='cascade', required=True)
    cost_line_id = fields.Many2one(
        'retaceo.internacion', 'Cost Line', readonly=True)
    order_id = fields.Many2one('purchase.order', string='Numero PO', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    quantity = fields.Float(
        'Cantidad', default=1.0,
        digits=0, required=True)
    unit_price = fields.Float(
        'Precio', default=1.0,
        digits=0, required=True)
    weight = fields.Float(
        'Peso', default=1.0,
        digits=dp.get_precision('Stock Weight'))
    volume = fields.Float(
        'Volumen', default=1.0)
    former_cost = fields.Float(
        'Costo', digits=dp.get_precision('Product Price'))
    former_cost_per_unit = fields.Float(
        'Former Cost(Per Unit)',compute='_compute_former_cost_per_unit', digits=0, store=True)
    additional_landed_cost = fields.Float(
        'Additional Landed Cost',
        digits=dp.get_precision('Product Price'))
    final_cost = fields.Float(
        'Final Cost',
        digits=0, store=True)

    porrateo_int = fields.Float(string="Porrateo/ GI", compute="_compute_porrateo_int", compute_sudo=True, store=True)
    vcif = fields.Float(string="V.CIF", compute="_compute_vcif", compute_sudo=True, store=True)
    porrateo_nac = fields.Float(string="Porrateo/ GN", compute="_compute_porrateo_nac", compute_sudo=True, store=True)
    costo_total = fields.Float(string="Costo Total", compute="_compute_costo_total", compute_sudo=True, store=True)
    costo_unitario = fields.Float(string="Costo Unitario", compute="_compute_costo_unitario",
                                  compute_sudo=True, store=True)

    @api.depends('former_cost', 'quantity')
    def _compute_former_cost_per_unit(self):
        for rec in self:
            rec.former_cost_per_unit = rec.former_cost / (rec.quantity or 1.0)

    @api.depends('cost_id.total_former_cost', 'porrateo_int', 'cost_id.amount_total', 'former_cost')
    def _compute_porrateo_int(self):
        for calculo in self:
            if calculo.cost_id.total_former_cost > 0.0:
                calculo.porrateo_int = (calculo.cost_id.amount_total / calculo.cost_id.total_former_cost) \
                                        * calculo.former_cost
            else:
                calculo.porrateo_int = 0.0

    @api.depends('porrateo_int', 'former_cost')
    def _compute_vcif(self):
        for calculo in self:
            calculo.vcif = calculo.former_cost + calculo.porrateo_int

    @api.depends('cost_id.total_vicf', 'porrateo_nac', 'cost_id.total_gastos', 'vcif')
    def _compute_porrateo_nac(self):
        for calculo in self:
            if calculo.cost_id.total_vicf > 0.0:
                calculo.porrateo_nac = (calculo.cost_id.total_gastos / calculo.cost_id.total_vicf) * calculo.vcif
            else:
                calculo.porrateo_nac = 0.0

    @api.depends('vcif', 'porrateo_nac')
    def _compute_costo_total(self):
        for calculo in self:
            calculo.costo_total = calculo.porrateo_nac + calculo.vcif

    @api.depends('vcif', 'quantity')
    def _compute_costo_unitario(self):
        for calculo in self:
            calculo.costo_unitario = round((calculo.costo_total / calculo.quantity), 2)


class GastosNacionales(models.Model):
    _name = 'retaceo.nacionales'
    _description = 'Average Landed cost Lines'

    gastos_line = fields.Many2one('retaceo.poliza')
    invoice_id = fields.Many2one('account.move', 'Factura', required=True,
                                 domain=[('move_type', '=', 'in_invoice'), ('state', '=', 'posted')])
    reference = fields.Char(string='Referencia', required=False)
    total = fields.Float(string='Total', required=False)

    @api.onchange('invoice_id')
    def onchange_product_id(self):
        self.reference = self.invoice_id.ref or ''
        self.total = self.invoice_id.amount_untaxed or 0.0

class AverageLandedCostLines(models.Model):
    _name = 'average.landed.cost.lines'
    _description = 'Average Landed cost Lines'

    line_id = fields.Many2one('retaceo.poliza')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    quantity = fields.Float('Quantity')
    additional_landed_cost_sum = fields.Float('Sum')
    total_costo = fields.Float('Total')
    average_landed_cost = fields.Float('Average Landed Cost')

    def action_entry(self):
        for rec in self:
            for line in rec.line_id:
                debit = rec.total_costo
                credit = rec.total_costo
                move = {
                    'name': '/',
                    'journal_id': line.journal_id.id,
                    'date': line.fecha,
                    'ref': line.name,

                    'line_ids': [(0, 0, {
                        'name': rec.product_id.name or '/',
                        'debit': debit,
                        'account_id': rec.product_id.debit_account_id.id,
                        'partner_id': line.order_id.partner_id.id,
                    }), (0, 0, {
                        'name': rec.product_id.name or '/',
                        'credit': credit,
                        'account_id': rec.product_id.credit_account_id.id,
                        'partner_id': line.order_id.partner_id.id,
                    })]
                }
                move_id = line.env['account.move'].create(move)
                move_id.post()
                return line.write({'state': 'progress', 'move_id': move_id.id})

