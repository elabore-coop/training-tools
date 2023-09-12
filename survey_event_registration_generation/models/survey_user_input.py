
import logging
import textwrap
import uuid

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def save_lines(self, question, answer, comment=None):
        old_answers = self.env['survey.user_input.line'].search([
            ('user_input_id', '=', self.id),
            ('question_id', '=', question.id)
        ])
        if question.question_type == 'event_product':
            self._save_event_product(question, old_answers, answer)
        elif question.question_type == 'event':
            self._save_event(question, old_answers, answer)
        else:
            return super().save_lines(question, answer, comment)

    
    def _save_event_product(self, question, old_answers, answer):
        vals = self._get_line_answer_values(question, answer, question.question_type)
        vals['value_event_product'] = int(vals['value_event_product'])
        if old_answers:
            old_answers.write(vals)
            return old_answers
        else:
            return self.env['survey.user_input.line'].create(vals)
        
    def _save_event(self, question, old_answers, answer):
        vals = self._get_line_answer_values(question, answer, question.question_type)
        vals['value_event'] = int(vals['value_event'])
        if old_answers:
            old_answers.write(vals)
            return old_answers
        else:
            return self.env['survey.user_input.line'].create(vals)