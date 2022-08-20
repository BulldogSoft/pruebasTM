
{
    'name': 'POS Custom Ticket TM',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Este modulo permite customizar el ticket de pos para TM',
    'website': 'www.bulldogsoft.com',
    'author': 'Bulldogsoft/Kevin Cruz',
    'description': "Personalización de ticket",
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/assets.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
}
