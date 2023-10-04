# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    generate_speaker = fields.Boolean(
        help="Generate speaker for selected event",
    ) #Field to check if user wants to generate a speaker on survey submit
