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
from odoo import fields, models, api, _

class Partner(models.Model):
    _inherit = 'res.partner'

    munic_id = fields.Many2one('res.municipality', _('Municipality'),ondelete='restrict')
    
    #@api.onchange('state_id')
    def _onchange_state_id(self):
        if not self.country_id:
            self.country_id = self.state_id.country_id
        if self.state_id:
            return {'domain': {'munic_id': [('dpto_id', '=', self.state_id.id)]}}
        else:
            return {'domain': {'munic_id': []}}
    
    @api.onchange('munic_id')
    def _onchange_munic_id(self):
        if not self.state_id:
            self.state_id = self.munic_id.dpto_id
            
    