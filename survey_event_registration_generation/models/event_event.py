from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    visible_in_survey = fields.Boolean('Visible in survey', related='stage_id.visible_in_survey', readonly=True, 
        help="""Events in step configured as 'visible in survey'.""")



    def get_events_from_event_products(self, product_ids=None, only_visible_in_survey=False):
        """Search events in stage filtered by product present in ticket..         

        Args:
            product_ids (list[product.product ids], optional): to filter only events with tickets using product in this list. Defaults to None.

        Returns:
            event.event: Events
        """
        event_search = []
        if product_ids:
            event_tickets = self.env['event.event.ticket'].search([('product_id','in',product_ids)])
            event_search.append(('event_ticket_ids','in',event_tickets.ids))

        if only_visible_in_survey:
            event_search.append(('visible_in_survey','=',True))
        
        return self.env['event.event'].search(event_search)
        