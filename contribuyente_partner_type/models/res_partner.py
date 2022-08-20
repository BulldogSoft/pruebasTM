# Copyright 2021 Guillermo Guevara <guillermoguevara@bulldogsoft.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    contribuyente_type = fields.Selection(
        selection="_selection_contribuyente_type",
        string="Clasificación",
        default=lambda self: self._default_contribuyente_type(),
    )

    def _selection_contribuyente_type(self):
        field = "contribuyente_type"
        return self.env["account.fiscal.position"].fields_get(allfields=[field])[field][
            "selection"
        ]

    @api.model
    def _default_contribuyente_type(self):
        return self.env.company.default_contribuyente_type

    @api.model
    def _commercial_fields(self):
        return super(ResPartner, self)._commercial_fields() + ["contribuyente_type"]
