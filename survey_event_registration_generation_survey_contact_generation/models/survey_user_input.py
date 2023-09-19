
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
    

    def _mark_done(self):
        res = super()._mark_done()
        
        """Generate registration when the survey is submitted"""
        for user_input in self.filtered(
            lambda r: r.survey_id.generate_registration and not self.registration_id
        ):
            vals = user_input._prepare_registration()
            
            registration = self.env["event.registration"].create(vals)
            self._create_registration_post_process(registration)
            self.update({"registration_id": registration.id})
        res = super()._mark_done()

        # after all, set partner id of registration as the partner of user input
        for user_input in self:
            if user_input.registration_id and user_input.partner_id:
                user_input.registration_id.partner_id = user_input.partner_id
        return res
