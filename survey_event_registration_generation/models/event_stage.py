from odoo import models, fields, api


class EventStage(models.Model):
    _inherit = 'event.stage'

    visible_in_survey = fields.Boolean('Visible in surveys')