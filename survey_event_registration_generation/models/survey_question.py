from email.policy import default
from odoo import models, fields, api


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    question_type = fields.Selection(
        selection_add=[('event_product', 'Event product'),('event', 'Event'),('multiple_event_products', 'Multiple event products')]) #event_product : List product used in tickets of visible events
                                                                               #event : List events visible in surveys

    show_events_and_event_products_only_visible_in_survey = fields.Boolean('Show events or event products in step visible in survey', 
        help="""In event step configuration, you can check 'Visible in surveys'. 
        If this option is checked, 
        If question display events, they are filtered with only events in step 'Visible in survey'. 
        If question display event products, they are filtered with only products of events in step 'Visible in survey'.""")
                                                                                   

    event_product_question_id = fields.Many2one(
        'survey.question', string="Event product question", copy=False, compute="_compute_event_product_question_id",
        store=True, readonly=False, help="If you specify question of event product, only events of selected product will be proposed.",
        domain="[('survey_id', '=', survey_id), \
                 '&', ('question_type', 'in', ['event_product','multiple_event_products']), \
                 '|', \
                     ('sequence', '<', sequence), \
                     '&', ('sequence', '=', sequence), ('id', '<', id)]") #event product question, used by event question, to filter list of events
    
    event_registration_allowed_field_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        compute="_compute_event_registration_allowed_field_ids",
    ) #fields of event registration, proposed in question, to associate answer to good event registration field, during event registration creation
    event_registration_field = fields.Many2one(
        string="Event registration field",
        comodel_name="ir.model.fields",
        domain="[('id', 'in', event_registration_allowed_field_ids)]",
    ) #field of event registration selected, used in event registration creation

    @api.depends("question_type")
    def _compute_event_registration_allowed_field_ids(self):
        """propose all event registration fields corresponding to selected question type
        """
        type_mapping = {
            "char_box": ["char", "text"],
            "text_box": ["html"],
            "numerical_box": ["integer", "float", "html", "char"],
            "date": ["date", "text", "char"],
            "datetime": ["datetime", "html", "char"],
            "simple_choice": ["many2one", "html", "char"],
            "multiple_choice": ["many2many", "html", "char"],            
        }
        for record in self:
            if record.question_type == "event":
                record.event_registration_allowed_field_ids = self.env["ir.model.fields"].search(
                    [
                        ("model", "=", "event.registration"),
                        ("name", "=", "event_id"),
                    ]
                ).ids
            
            record.event_registration_allowed_field_ids = self.env["ir.model.fields"].search(
                    [
                        ("model", "=", "event.registration"),
                        ("ttype", "in", type_mapping.get(record.question_type, [])),
                    ]
                ).ids
            
    
    @api.depends('question_type')
    def _compute_event_product_question_id(self):
        """ Used as an 'onchange' : Reset the event product question if user change question type
            Avoid CacheMiss : set the value to False if the value is not set yet."""
        for question in self:
            if not question.question_type == 'event' or question.event_product_question_id is None:
                question.event_product_question_id = False
    
