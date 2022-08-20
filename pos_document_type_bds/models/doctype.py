# copyright 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class PosDocumentType(models.Model):
    _name = 'pos.doc.type'
    _description = 'Tipo de Documento POS'

    name = fields.Char(
        string='Tipo de Documento',
        required=True)
    code = fields.Char(string='Código', required=True)







