# -*- coding: utf-8 -*-
#################################################################################
from odoo import api, models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    is_dcl = fields.Boolean(string="Es DCL?",)

    dcl_serie = fields.Char(string="N° Serie", required=False,)
    dcl_resolucion = fields.Char(string="Resolución", required=False,)
    dcl_documento = fields.Char(string="N° Documento", required=False,)