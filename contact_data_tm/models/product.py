# copyright 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class TechDataProductTemplate(models.Model):

    _inherit = 'product.template'

    barcode = fields.Char(
        string='Barcode',
        required=False)

    product_type = fields.Many2one(
        comodel_name='product.type',
        string='Clase',
        required=False)

    @api.onchange('name')
    def name_upper(self):
        for rec in self:
            if rec.name:
                name_upper = str(rec.name)
                rec.name = name_upper.upper()


class TechDataProductProduct(models.Model):

    _inherit = 'product.product'

    product_type = fields.Many2one(
        comodel_name='product.type',
        string='Clase',
        required=False)

    barcode = fields.Char(
        string='Barcode',
        required=False)

    @api.onchange('name')
    def name_upper(self):
        for rec in self:
            if rec.name:
                name_upper = str(rec.name)
                rec.name = name_upper.upper()


class ProductType(models.Model):
    _name = 'product.type'
    _description = 'Clientes'

    name = fields.Char(
        string='Tipo de Producto',
        required=True)



        





