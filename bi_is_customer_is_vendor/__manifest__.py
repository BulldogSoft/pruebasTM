# -*- coding: utf-8 -*-

{
	'name': "Opción de cliente o proveedor en Contactos",
	'version': "14.0.0.1",
	'category': "Extra Tools",
	'summary': "Puede ordenar sus contactos asignandoles si son clientes o proveedores, esta opción ayuda a filtrar en las órdenes de compras y ventas dentro del sitema. " ,
	'description':	"""
					Puede ordenar sus contactos asignandoles si son clientes o proveedores, esta opción ayuda a filtrar en las órdenes de compras y ventas dentro del sitema.
					""",
	'author': "Bulldogsoft-Gerson Carranza",
	"website" : "https://www.bulldogsoft.com",
	"currency": 'EUR',
	'depends': ['base','sale_management','purchase','contacts'],
	'data': [
				'views/res_partner_view.xml',
			],
	'demo': [],
	'qweb': [],
	'installable': True,
	'auto_install': False,
	'application': False,
	"images":['static/description/Banner.png'],
}
