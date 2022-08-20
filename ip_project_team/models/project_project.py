# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MeetingCountProject(models.Model):
    _inherit = 'project.project'

    team_id = fields.Many2one('project.team', string='Team Name')
    team_members = fields.Many2many(
        'res.users', string='Members',
        related='team_id.team_members')

    @api.onchange('team_id')
    def onchange_team_id(self):
        if self.team_id:
            self.user_id = self.team_id.user_id.id


class AssignTaskToMembers(models.Model):
    _inherit = 'project.task'

    team_members = fields.Many2many(
        'res.users', related="project_id.team_members")
    manager = fields.Many2one('res.users', related="project_id.user_id")
    user_id = fields.Many2one(
        'res.users', string='Assigned to',
        domain="['|', ('id', 'in', team_members), ('id', '=', manager)]",
        index=True, tracking=True)

    def action_assign_to_me(self):
        if self.env.user.id in self.project_id.team_members.ids + self.project_id.user_id.ids:
            return super(AssignTaskToMembers, self).action_assign_to_me()
        else:
            raise ValidationError(_("You have no permission to assign task you because of you are not part of %s team ") % (self.project_id.team_id.name))

    @api.onchange('user_id', 'project_id')
    def _onchange_users(self):
        if self._context.get('active_id') or self.user_id:
            project = self.env['project.project'].search(
                [('id', '=', self._context.get('active_id'))])
            user_ids = project.team_members + project.user_id
        elif self.project_id:
            user_ids = self.project_id.team_members + self.project_id.user_id
        else:
            user_ids = self.env['res.users'].search([])
        return {'domain': {'user_id': [('id', 'in', user_ids.ids)]}}

    @api.model
    def create(self, vals):
        result = super(AssignTaskToMembers, self).create(vals)
        if result.project_id and result.user_id:
            if result.user_id.id not in result.project_id.team_members.ids + result.project_id.user_id.ids:
                raise ValidationError(_("You can assign task to user from %s team only.") % (result.project_id.team_id.name))
        return result

    def write(self, vals):
        result = super(AssignTaskToMembers, self).write(vals)
        if self.project_id and self.user_id:
            if self.user_id.id not in self.project_id.team_members.ids + self.project_id.user_id.ids:
                raise ValidationError(_("You can assign task to user from %s team only.") % (self.project_id.team_id.name))
        return result
