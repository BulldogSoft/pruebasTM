# Copyright 2021 Guillermo Guevara <guillermoguevara@bulldogsoft.com>
# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

{
    "name": "Clasificación de Contribuyente BDS",
    "version": "13.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://www.bulldogsoft.com",
    "author": "BulldogSoft",
    "license": "Other proprietary",
    "application": False,
    "installable": True,
    "currency": 'USD',
    "price": 150.00,
    "development_status": "Production/Stable",
    "depends": ["account", "l10n_sv"],
    "data": [
        "data/fiscal_position_data.xml",
        "views/res_company.xml",
        "views/res_partner.xml",
        "views/contribuyente_partner_type.xml",
    ],
}
