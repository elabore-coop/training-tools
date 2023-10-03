from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_event_products_visible_in_survey(self):
        events = self.env['event.event'].get_events_visible_in_survey()
        products = set()
        for event in events:
            for ticket in event.event_ticket_ids:
                products.add(ticket.product_id)
        return list(products)