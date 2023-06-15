# Copyright 2018 Nicolas JEUDY
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class EventEvent(models.Model):
    _inherit = ["event.event"]

    speaker_ids = fields.One2many("event.speaker", "event_id", string="Speakers")
    nb_speakers = fields.Integer(
        string="Number of speaker", readonly=True, compute="_compute_nb_speakers"
    )

    @api.depends("speaker_ids")
    def _compute_nb_speakers(self):
        for event in self:
            event.nb_speakers = len(event.speaker_ids)


class EventDiscipline(models.Model):
    _name = "event.discipline"
    _description = "Discipline"

    name = fields.Char("Name")


class EmployeeDiscipline(models.Model):
    _inherit = "hr.employee"

    discipline_ids = fields.Many2many("event.discipline", string="Disciplines")
