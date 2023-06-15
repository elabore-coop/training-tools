# Copyright 2018 Nicolas JEUDY
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# import barcode
# from barcode.writer import ImageWriter
import base64
import logging
from io import BytesIO
import re
import unicodedata

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class HrEmployee(models.Model):
    _name = "event.speaker"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _get_default_stage_id(self):
        event_stages = self.env["event.speaker.stage"].search([])
        return event_stages[0] if event_stages else False

    name = fields.Char("Name", compute="_compute_name", store="True")
    employee_id = fields.Many2one("hr.employee", string="Speaker")
    discipline_id = fields.Many2one("event.discipline", string="Discipline")
    working_hours = fields.Float("Working hours")
    has_extra = fields.Boolean("Has Extra ?")
    event_id = fields.Many2one("event.event", string="Event")
    stage_id = fields.Many2one(
        "event.speaker.stage",
        ondelete="restrict",
        default=_get_default_stage_id,
        group_expand="_read_group_stage_ids",
        tracking=True,
    )
    discipline_ids = fields.Many2many(
        "event.discipline", string="discipline", related="employee_id.discipline_ids"
    )

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env["event.speaker.stage"].search([])

    @api.depends("employee_id", "discipline_id")
    def _compute_name(self):
        for record in self:
            name = ""
            if record.employee_id:
                name += record.employee_id.name
            if record.discipline_id:
                name += " (%s)" % record.discipline_id.name
            record.name = name
