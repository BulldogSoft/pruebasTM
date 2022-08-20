# Copyright 2021 Guillermo Guevara <guillermoguevara@bulldogsoft.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    default_contribuyente_type = fields.Selection(
        selection="_selection_contribuyente_type",
        string="Clasificación:",
    )

    def _selection_contribuyente_type(self):
        field = "contribuyente_type"
        return self.env["account.fiscal.position"].fields_get(allfields=[field])[field][
            "selection"
        ]
