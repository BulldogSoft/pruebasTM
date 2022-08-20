# -*- coding: utf-8 -*-
#################################################################################
#################################################################################
{
   'name':"Cheques BDS TM",
   'author':"Bulldogsoft/Kevin Cruz",
   'category':"Account",
   'summary':"""" Genera cheques con diferentes formatos """,
   'website':"http://www.bulldogsoft.com",
   'description':"""Cheques con diferentes formatos""",
   'version' : '12.0.1.0',
   'depends' : ['account', 'payment',],
   'data':[
            'report/cheque_interno.xml',
            'report/cheque_config.xml',
            'report/cheque_formatos.xml',
            'views/account_payment.xml',
  ],
    'license'     : 'AGPL-3',
    'installable':True,
    'application':True,
    'auto_install':False,
}
