# copyright 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_product_accounts(self):
        branch = self.env.context.get('user_id', self.env.user.branch_id)

        if self.type != 'service':
            return {
                'income': branch.product_income_account or self.property_account_income_id or
                          self.categ_id.property_account_income_categ_id,
                'expense': branch.product_expense_account or self.property_account_expense_id or
                           self.categ_id.property_account_expense_categ_id
            }

        if self.type == 'service':
            return {
                'income': self.property_account_income_id or self.categ_id.property_account_income_categ_id,
                'expense': self.property_account_expense_id or self.categ_id.property_account_expense_categ_id
            }


