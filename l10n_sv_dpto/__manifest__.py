# -*- coding: utf-8 -*-
#############################################################################
#
#    BulldogSoft El Salvador
#    Copyright (C) 2019-TODAY BulldogSoft (https://www.bulldogsoft.com)
#    Author: Guillermo Guevara @ BulldgSoft, (hello@bulldogsoft.com)
#            Gerson Carranza @ BulldgSoft, (hello@bulldogsoft.com)
#            Kevin Cruz @ BulldgSoft, (hello@bulldogsoft.com)
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': "Departamentos y Municipios de El Salvador",
    'summary': """Permite generar el reporte de Departamentos y Municipios de El Salvador""",
    'description': """
        Permite generar el reporte de  Departamentos y Municipios de El Salvador
        """,
    'author': "Bulldogsoft",
    'website': "http://www.bulldogsoft.com",
    'price': 50.00,
    'currency': 'USD',
    'license': 'GPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'General',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base',
                'sales_team',
                'sale'],
    # always loaded
    'data': [
        'data/res.country.state.csv',
        'data/res.municipality.csv',
        'views/res_municipality.xml',
        'views/res_partner.xml',
        'views/res_bank.xml',
        'security/ir.model.access.csv',
   # 'views/view_res_company.xml',
    #'views/view_res_partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    #'demo.xml',
    ],
}