from odoo import models, fields, api


class EventStage(models.Model):
    _inherit = 'event.stage'

    visible_in_survey = fields.Boolean('Visible in surveys') #if checked, only events on this stage are visible in surveys