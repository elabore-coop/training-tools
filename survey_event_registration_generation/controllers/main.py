# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.survey.controllers import main
from odoo.http import request
from odoo import http

class Survey(main.Survey):

    @http.route(['/survey_event/get_events_from_product'], type='json', auth="public", methods=['POST'])
    def get_events_from_product(self, product_ids, only_visible_in_survey, **kw):    
        """
        Called from survey_form.js when event product answer change, reload event list
        """    
        if not product_ids:
            return []
        events = request.env['event.event'].sudo().get_events_from_event_products(product_ids, only_visible_in_survey=only_visible_in_survey)
        return [{'id':event.id,'name':event.name} for event in events]


    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):        
        result = super(Survey, self)._prepare_survey_data(survey_sudo, answer_sudo, **post)

        result['event_products'] = {}
        result['events'] = {}

        for question in answer_sudo.predefined_question_ids:      
            if question.question_type == 'event_product':   
                # set event products answers (by question)          
                if question.show_events_and_event_products_only_visible_in_survey:
                    result['event_products'][question.id] = request.env['product.product'].sudo().search([('detailed_type','=','event'),('visible_in_survey','=',True)]) 
                else:
                    result['event_products'][question.id] = request.env['product.product'].sudo().search([('detailed_type','=','event')]) 

            if question.question_type == 'event':

                # set events answers (by question)
                if question.event_answer_filter == 'all':
                    if question.show_events_and_event_products_only_visible_in_survey:
                        result['events'][question.id] = request.env['event.event'].sudo().search([('visible_in_survey','=',True)])
                    else:
                        result['events'][question.id] = request.env['event.event'].sudo().search([])
                else:
                    if question.event_answer_filter ==  'event_product':
                        event_products_ids = [question.event_filter_event_product_id.id]
                    elif question.event_answer_filter ==  'event_product_question':
                        event_products_ids = self._get_answer_event_product(question.event_product_question_id, answer_sudo).id
                    result['events'][question.id] = request.env['event.event'].sudo().get_events_from_event_products(event_products_ids, 
                                                                                                                     only_visible_in_survey=question.show_events_and_event_products_only_visible_in_survey)

        return result

    def _get_answer_event_product(self, question, answer_sudo):
        """return value(s) selected in for Event Product question.
        Question can be event_product (only one event product selected)
        or multiple_event_products (several event products can be selected)

        Args:
            question (survey.question): Event product question
            answer_sudo (survey.user.input)

        Returns:
            List<product.product>: List of selected event products
        """
        for user_input_line in answer_sudo.user_input_line_ids:
            if user_input_line.question_id == question:
                if question.question_type == 'event_product':
                    return [user_input_line.value_event_product]
                if question.question_type == 'multiple_event_products':
                    return user_input_line.value_multiple_event_products

