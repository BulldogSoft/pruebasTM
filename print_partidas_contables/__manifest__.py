# -*- coding: utf-8 -*-
#################################################################################
# Author      : BulldogSoft (<https://bulldogsoft.com/>)
# Copyright(c): 2019 bulldogsoft.com
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
#################################################################################
{
  "name"                 :  "Imprimir Partidas Contables",
  "summary"              :  "Este modulo permite imprimir partidas contables en una sola lista",
  "category"             :  "Accounting",
  "version"              :  "12.0",
  "author"               :  "Kevin Cruz / bds",
  "license"              :  "OPL-1",
  "website"              :  "https://bulldogsoft.com",
  "description"          :  """
  Este modulo agrega la opcion de imprimir en la seleccion de partidas contables.
  """,
  "depends"              :  [
                             'account'
                            ],
  "data"                 :  [
                             'views/template_partidas_contables.xml',
                             'views/reportes.xml',
                            ],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}