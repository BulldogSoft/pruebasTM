# Copyright 2021 Guillermo Guevara <guillermoguevara@bulldogsoft.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class TestContribuyentePartnerType(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestContribuyentePartnerType, cls).setUpClass()
        # MODELS
        cls.res_partner_model = cls.env["res.partner"]
        cls.account_move_model = cls.env["account.move"]
        cls.fiscal_position_model = cls.env["account.fiscal.position"]
        # INSTANCES
        # Company
        cls.company_main = cls.env.ref("base.main_company")
        cls.company_main.default_contribuyente_type = "otro"
        # Fiscal Positions
        cls.fiscal_position_test = cls.fiscal_position_model.create(
            {
                "name": "Test",
                "auto_apply": False,
                "contribuyente_type": False,
                "sequence": 1,
            }
        )
        cls.fiscal_position_empty = cls.fiscal_position_model.create(
            {
                "name": "Empty",
                "auto_apply": True,
                "contribuyente_type": False,
                "sequence": 2,
            }
        )
        cls.fiscal_position_otro = cls.fiscal_position_model.create(
            {
                "name": "otro",
                "auto_apply": True,
                "contribuyente_type": "Otro",
                "sequence": 3,
            }
        )
        cls.fiscal_position_mediano = cls.fiscal_position_model.create(
            {
                "name": "mediano",
                "auto_apply": True,
                "contribuyente_type": "Mediano",
                "sequence": 4,
            }
        )
        cls.fiscal_position_grande = cls.fiscal_position_model.create(
            {
                "name": "grande",
                "auto_apply": True,
                "contribuyente_type": "Grande",
                "sequence": 5,
            }
        )
        # Partners
        cls.partner_01 = cls.env.ref("base.res_partner_1")
        cls.partner_01.write({"contribuyente_type": False})
        cls.partner_02 = cls.env.ref("base.res_partner_2")
        cls.partner_02.write({"contribuyente_type": "otro"})
        cls.partner_03 = cls.env.ref("base.res_partner_3")
        cls.partner_03.write({"contribuyente_type": "mediano"})
        cls.partner_04 = cls.env.ref("base.res_partner_4")
        cls.partner_04.write(
            {
                "contribuyente_type": "grande",
                "property_account_position_id": cls.fiscal_position_test.id,
            }
        )
        cls.partner_05 = cls.env.ref("base.res_partner_10")
        cls.partner_05.write({"contribuyente_type": "otro"})

    @classmethod
    def _invoice_sale_create(cls, partner):
        invoice_id = cls.account_move_model.create(
            {
                "company_id": cls.company_main,
                "partner_id": partner,
                "type": "in_invoice",
            }
        )
        invoice_id._onchange_partner_id()
        return invoice_id

    def test_01(self):
        partner_id = self.res_partner_model.create({"name": "contribuyente test"})
        self.assertEqual(partner_id.contribuyente_type, "otro")
        fiscal_position_id = self.fiscal_position_model.create(
            {"name": "contribuyente test", "auto_apply": True}
        )
        self.assertEqual(fiscal_position_id.contribuyente_type, "otro")

    def test_02(self):
        invoice_01 = self._invoice_sale_create(self.partner_01)
        self.assertEqual(invoice_01.fiscal_position_id, self.fiscal_position_empty)
        invoice_02 = self._invoice_sale_create(self.partner_02)
        self.assertEqual(invoice_02.fiscal_position_id, self.fiscal_position_otro)
        invoice_03 = self._invoice_sale_create(self.partner_03)
        self.assertEqual(invoice_03.fiscal_position_id, self.fiscal_position_mediano)
        invoice_04 = self._invoice_sale_create(self.partner_04)
        self.assertEqual(invoice_04.fiscal_position_id, self.fiscal_position_grande)
        invoice_05 = self._invoice_sale_create(self.partner_04)
        self.assertEqual(invoice_05.fiscal_position_id, self.fiscal_position_test)

    def test_03(self):
        fiscal_position_otro_country = self.fiscal_position_model.create(
            {
                "name": "otro with country",
                "auto_apply": True,
                "contribuyente_type": "otro",
                "country_id": self.env.ref("base.us").id,
            }
        )
        invoice_06 = self._invoice_sale_create(self.partner_05)
        self.assertEqual(invoice_06.fiscal_position_id, fiscal_position_otro_country)
