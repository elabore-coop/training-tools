
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

    registration_id = fields.Many2one('event.registration', 'Event registration') #registration created automaticaly on survey post

    event_id = fields.Many2one('event.event', 'Event', compute='compute_event_id', store=True) #related event - answer of "event" question

    event_product_id = fields.Many2one('product.product', 'Event product', compute='compute_event_product_id', store=True) #related event product - answer of "event product" question

    @api.depends('user_input_line_ids')
    def compute_event_id(self):
        """set event_id as answer of "event" question
        """
        for user_input in self:
            for user_input_line in user_input.user_input_line_ids:
                if user_input_line.answer_type == 'event':
                    user_input.event_id = user_input_line.value_event
                    break

    @api.depends('user_input_line_ids')
    def compute_event_product_id(self):
        """set event_product_id as answer of "event product" question
        """
        for user_input in self:
            for user_input_line in user_input.user_input_line_ids:
                if user_input_line.answer_type == 'event_product':
                    user_input.event_product_id = user_input_line.value_event_product
                    break

    def save_lines(self, question, answer, comment=None):
        """
            Inherit save_lines method, called after each answer
            to save selected event or event_product in user_input.line
            depending on the question type
        """
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
        """
            Save event product to user_input.line
        """
        vals = self._get_line_answer_values(question, answer, question.question_type)
        if 'value_event_product' in vals and vals['value_event_product'].isnumeric():
            vals['value_event_product'] = int(vals['value_event_product'])
        else:
            vals['value_event_product'] = 0
        if old_answers:
            old_answers.write(vals)
            return old_answers
        else:
            return self.env['survey.user_input.line'].create(vals)
        
    def _save_event(self, question, old_answers, answer):
        """
            Save event to user_input.line
        """
        vals = self._get_line_answer_values(question, answer, question.question_type)
        if 'value_event' in vals and vals['value_event'].isnumeric():
            vals['value_event'] = int(vals['value_event'])
        else:
            vals['value_event'] = 0
        if old_answers:
            old_answers.write(vals)
            return old_answers
        else:
            return self.env['survey.user_input.line'].create(vals)
        
    def _prepare_registration(self):
        """Extract registration values from the answers"""
        
        elegible_inputs = self.user_input_line_ids.filtered(
            lambda x: x.question_id.event_registration_field and not x.skipped
        )

        vals = {}
        for line in elegible_inputs:
            if line.question_id.event_registration_field.ttype == 'many2one':
                vals[line.question_id.event_registration_field.name] = line[f"value_{line.answer_type}"].id
            else:
                vals[line.question_id.event_registration_field.name] = line[f"value_{line.answer_type}"]
     
        
        return vals

    def _create_registration_post_process(self, registration):
        """After creating the event registration send an internal message with the input link"""
        registration.message_post_with_view(
            "mail.message_origin_link",
            values={"self": registration, "origin": self},
            subtype_id=self.env.ref("mail.mt_note").id,
        )

    def _mark_done(self):
        """Generate registration when the survey is submitted"""
        for user_input in self.filtered(
            lambda r: r.survey_id.generate_registration and not self.registration_id
        ):
            vals = user_input._prepare_registration()

            # check doublon : if old draft registration already exists : update it
            email = vals.get('email')
            event_id = vals.get('event_id')
            old_registration = False
            if email and event_id:
                old_registration = self.env["event.registration"].search([('email','=',email),('event_id','=',event_id)])
                if old_registration:
                    old_registration = old_registration[0]
                    if old_registration.state == 'draft':
                        registration = old_registration
                        registration.write(vals)
                        registration.message_post_with_view(
                            "mail.message_origin_link",
                            values={"edit":True, "self": registration, "origin": user_input},
                            subtype_id=self.env.ref("mail.mt_note").id,
                        )

            if not old_registration:
                registration = self.env["event.registration"].create(vals)
                self._create_registration_post_process(registration)
                
            self.update({"registration_id": registration.id})
        res = super()._mark_done()

        # after all, set partner id of registration as the partner of user input
        for user_input in self:
            if user_input.registration_id and user_input.partner_id:
                user_input.registration_id.partner_id = user_input.partner_id
        return res
