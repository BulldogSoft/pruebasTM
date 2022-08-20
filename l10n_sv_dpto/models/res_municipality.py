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
from odoo import fields, models, api, exceptions, _

class Departamento(models.Model):
  _name = "res.municipality"
  _descrition = _("Municipality")
  
  name = fields.Char(_("Name"), required=True, help=_("Name of municipality"), translate=True)
  code = fields.Char(_("Code"), required=True, help='Code of municipality')
  dpto_id = fields.Many2one('res.country.state',_("State"), required=True, help=_("State"))

  def copy(self, default=None):
      default = dict(default or {})
      
      copied_count = self.search_count(
          [('name', '=like', _(u"Copy of {}%").format(self.name))])
      if not copied_count:
          new_name = _(u"Copy of {}").format(self.name)
      else:
          new_name = _(u"Copy of {} ({})").format(self.name, copied_count)
          
      copied_count = self.search_count(
          [('code', '=like', _(u"Copy of {}%").format(self.code))])
      if not copied_count:
          new_code = _(u"Copy of {}").format(self.code)
      else:
          new_code = _(u"Copy of {} ({})").format(self.code, copied_count)
    
      default['name'] = new_name
      default['code'] = new_code
      return super(Departamento, self).copy(default)
        
  _sql_constraints = [
    (
      'name_code_unique',
      'UNIQUE(name,code)',
      _('The name must be unique')
    )
  ]
  