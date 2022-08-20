# copyright 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    empleado = fields.Many2one(
        'hr.employee',
        string='Preparado Por',
        required=False
        #,domain=[('department_id.name', '=', 'Logística')]
        )

        





