# -*- coding: utf-8 -*-
from odoo import models, fields


class ProjectTeamManage(models.Model):
    _name = 'project.team'
    _description = "Project Team"

    name = fields.Char(string='Team Name', required=True)
    user_id = fields.Many2one('res.users', required=True)
    team_members = fields.Many2many('res.users')
