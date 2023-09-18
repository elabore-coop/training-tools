from odoo import models, fields, api


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    question_type = fields.Selection(
        selection_add=[('event_product', 'Event product'),('event', 'Event')])
    

    event_product_question_id = fields.Many2one(
        'survey.question', string="Event product question", copy=False, compute="_compute_event_product_question_id",
        store=True, readonly=False, help="If you specify question of event product, only events of selected product will be proposed.",
        domain="[('survey_id', '=', survey_id), \
                 '&', ('question_type', '=', 'event_product'), \
                 '|', \
                     ('sequence', '<', sequence), \
                     '&', ('sequence', '=', sequence), ('id', '<', id)]")
    
    event_registration_allowed_field_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        compute="_compute_event_registration_allowed_field_ids",
    )
    event_registration_field = fields.Many2one(
        string="Event registration field",
        comodel_name="ir.model.fields",
        domain="[('id', 'in', event_registration_allowed_field_ids)]",
    )

    @api.depends("question_type")
    def _compute_event_registration_allowed_field_ids(self):
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
                record.event_registration_allowed_field_ids = (
                self.env["ir.model.fields"]
                .search(
                    [
                        ("model", "=", "event.registration"),
                        ("name", "=", "event_id"),
                    ]
                )
                .ids
            )
            record.event_registration_allowed_field_ids = (
                self.env["ir.model.fields"]
                .search(
                    [
                        ("model", "=", "event.registration"),
                        ("ttype", "in", type_mapping.get(record.question_type, [])),
                    ]
                )
                .ids
            )
    

    @api.depends('question_type')
    def _compute_event_product_question_id(self):
        """ Used as an 'onchange' : Reset the event product question if user change question type
            Avoid CacheMiss : set the value to False if the value is not set yet."""
        for question in self:
            if not question.question_type == 'event' or question.event_product_question_id is None:
                question.event_product_question_id = False
    

class SurveyQuestionAnswer(models.Model):
    _inherit = "survey.question.answer"

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        if (
            not result.get("event_registration_field")
            or "event_registration_field_resource_ref" not in fields
        ):
            return result
        registration_field = self.env["ir.model.fields"].browse(result["event_registration_field"])
        # Otherwise we'll just use the value (char, text)
        if registration_field.ttype not in {"many2one", "many2many"}:
            return result
        res = self.env[registration_field.relation].search([], limit=1)
        if res:
            result["event_registration_field_resource_ref"] = "%s,%s" % (
                registration_field.relation,
                res.id,
            )
        return result

    @api.model
    def _selection_event_registration_field_resource_ref(self):
        return [(model.model, model.name) for model in self.env["ir.model"].search([])]

    event_registration_field = fields.Many2one(related="question_id.event_registration_field")
    event_registration_field_resource_ref = fields.Reference(
        string="Event registration field value",
        selection="_selection_event_registration_field_resource_ref",
    )

    @api.onchange("event_registration_field_resource_ref")
    def _onchange_event_registration_field_resource_ref(self):
        """Set the default value as the display_name, although we can change it"""
        if self.event_registration_field_resource_ref:
            self.value = self.event_registration_field_resource_ref.display_name or ""
