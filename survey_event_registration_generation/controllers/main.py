# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.survey.controllers import main
from odoo.http import request
from odoo import http

class Survey(main.Survey):

    @http.route(['/survey_event/get_events_from_product'], type='json', auth="public", methods=['POST'])
    def get_events_from_product(self, product_id, **kw):        
        if not product_id:
            return []
        events = request.env['event.event'].sudo().get_events_visible_in_survey(product_id)
        return [{'id':event.id,'name':event.name} for event in events]


    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        result = super(Survey, self)._prepare_survey_data(survey_sudo, answer_sudo, **post)
        result['event_products'] = request.env['product.product'].sudo().get_event_products_visible_in_survey()

        next_event_question = self._get_next_event_question(answer_sudo)
        if next_event_question:
            event_product_id = None
            if next_event_question.event_product_question_id:
                event_product_id = self._get_answer_event_product(next_event_question.event_product_question_id, answer_sudo).id
            result['events'] = request.env['event.event'].sudo().get_events_visible_in_survey(event_product_id)

        return result

    def _get_answer_event_product(self, question, answer_sudo):
        for user_input_line in answer_sudo.user_input_line_ids:
            if user_input_line.question_id == question:
                return user_input_line.value_event_product


    def _get_next_event_question(self, answer_sudo):
        future_question = False
        for question in answer_sudo.predefined_question_ids:            
            if question == answer_sudo.last_displayed_page_id:
                future_question = True
                continue
            if not future_question:
                continue
            if question.question_type == 'event':
                return question
