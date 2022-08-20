# Copyright 2020 WeDo Technology
# Website: http://wedotech-s.com
# Email: apps@wedotech-s.com
# Phone:00249900034328 - 00249122005009

{
    'name': "Sale Product Consumption Info",
    'version': '13.0.1.0',
    'license': 'OPL-1',
    'author': 'BDS/Gerson Carranza',
    'category': 'Sale',
    'sequence': 1,
    'depends': ['sale','stock'],
    'summary': """
       Show info in Sale lines to know available quantities, Last Week Consumption and Last Month Consumption for each location.
       """,
    'description': """
        RFQ and Sale Order
        Allow to show these information in Purchase Lines for each location:
            Quantity Available
            Last Week Consumption
            Last Month Consumption
        """,
    'data': [
        'views/sale_view.xml',
        'views/templates.xml',
    ],
    'qweb': ['static/src/xml/qty_at_date.xml'],
    'application': True,
}

