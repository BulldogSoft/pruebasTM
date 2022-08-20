# Copyright 2021 Guillermo Guevara <guillermoguevara@bulldogsoft.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.osv import expression


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    contribuyente_type = fields.Selection(
        selection=[("otros", "Otros Contribuyentes"),
                   ("mediano", "Mediano Contribuyente"),
                   ("grande", "Gran Contribuyente"),
                   ("sujexculido", "Sujeto Excluido"),
                   ("exento", "Exento"),
                   ("nosujeto", "No Sujeto"),
                   ("internacionales", "Internacional")],
        string="Clasificación",
        default=lambda self: self._default_contribuyente_type(),
    )

    @api.model
    def _default_contribuyente_type(self):
        return self.env.company.default_contribuyente_type

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self.env.context.get("contribuyente_type"):
            args = expression.AND(
                (
                    args,
                    [
                        (
                            "contribuyente_type",
                            "=",
                            self.env.context.get("contribuyente_type", False),
                        )
                    ],
                )
            )
        return super().search(
            args, offset=offset, limit=limit, order=order, count=count
        )

    @api.model
    def get_fiscal_position(self, partner_id, delivery_id=None):
        fiscal_type = False
        if partner_id:
            delivery = self.env["res.partner"].browse(delivery_id or partner_id)
            # Only type has been configured
            if (
                delivery.contribuyente_type
                and not delivery.property_account_position_id
            ):
                fiscal_type = delivery.contribuyente_type
        fp_id = super(
            AccountFiscalPosition, self.with_context(contribuyente_type=fiscal_type)
        ).get_fiscal_position(partner_id=partner_id, delivery_id=delivery_id)
        return fp_id
