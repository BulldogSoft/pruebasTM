# -*- encoding: utf-8 -*-
{
    "name": "Secuencia partidas TM",
    "version": "0.1",
    "author": "BDS/Gerson Carranza",
    "website": "https://bulldogsoft.com",
    "category": "accounting",
    'summary': """
        Genera una secuencia para cada tipo de partida, dependiendo de los campos colocados en la partida 
        ejemplo: D-CM223569
        D = Tipo de partida
        CM = Sucursal en la que esta ubicado el usuario
        22 = Año
        3569 = Correlativo     
    """,
    "depends": ['base', 'account', 'account_accountant', 'branch'],

    'data': [
        'data/sequence.xml',
        'views/account_move_view.xml',
    ],

    "installable": True,
}
