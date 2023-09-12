import logging
import textwrap
import uuid

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    answer_type = fields.Selection(
        selection_add=[('event_product', 'Event product'),('event', 'Event')])

    value_event = fields.Many2one('event.event', string="Event")
    value_event_product = fields.Many2one('product.product', string="Event product")

    def _compute_display_name(self):
        super()._compute_display_name()
        for line in self:
            if line.answer_type == 'event_product':
                line.display_name = line.value_event_product.name
            elif line.answer_type == 'event':
                line.display_name = line.value_event.name
          