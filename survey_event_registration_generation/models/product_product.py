from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    visible_in_survey = fields.Boolean('Visible in survey', compute='_compute_visible_in_survey', readonly=True, 
        help="""Events in step configured as 'visible in survey'.""")
    

    def _compute_visible_in_survey(self):
        #get all events in step 'visible in survey'
        product_ids = set()
        events = self.env['event.event'].search([('visible_in_survey','=',True)])
        for event in events:
            for ticket in event.event_ticket_ids:
                product_ids.add(ticket.product_id.id)
        for event_product in self:
            if event_product.id in product_ids:
                event_product.visible_in_survey = True
            else:
                event_product.visible_in_survey = False        

