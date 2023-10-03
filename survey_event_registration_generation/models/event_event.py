from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    def get_events_visible_in_survey(self, product_id=False):
        if product_id:
            event_tickets = self.env['event.event.ticket'].search([('product_id','=',product_id)])
            return self.env['event.event'].search([('stage_id.visible_in_survey','=',True),('event_ticket_ids','in',event_tickets.id)])
        return self.env['event.event'].search([('stage_id.visible_in_survey','=',True)])
        