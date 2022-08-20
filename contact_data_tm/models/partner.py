
from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('name')
    def name_upper(self):
        for rec in self:
            if rec.name:
                name_upper = str(rec.name)
                rec.name = name_upper.upper()

