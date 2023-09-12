from odoo import models, fields, api


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    question_type = fields.Selection(
        selection_add=[('event_product', 'Event product'),('event', 'Event')])
    

    event_product_question_id = fields.Many2one(
        'survey.question', string="Event ticket question", copy=False, compute="_compute_event_product_question_id",
        store=True, readonly=False, help="If you specify question of event product, only events of selected product will be proposed.",
        domain="[('survey_id', '=', survey_id), \
                 '&', ('question_type', '=', 'event_product'), \
                 '|', \
                     ('sequence', '<', sequence), \
                     '&', ('sequence', '=', sequence), ('id', '<', id)]")
    

    @api.depends('question_type')
    def _compute_event_product_question_id(self):
        """ Used as an 'onchange' : Reset the event ticket question if user change question type
            Avoid CacheMiss : set the value to False if the value is not set yet."""
        for question in self:
            if not question.question_type == 'event' or question.triggering_question_id is None:
                question.triggering_question_id = False
    