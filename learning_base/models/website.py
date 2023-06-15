import logging
from odoo import models

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    def sale_product_domain(self):
        # ['&', ('sale_ok', '=', True), ('website_id', 'in', (False, 1)), ('event_ok', '=', False)] 
        _logger.debug(super(Website, self).sale_product_domain())
        #return ['&'] + super(Website, self).sale_product_domain() + [('event_ok', '=', False)]
        return [('sale_ok', '=', True), ('website_id', 'in', (False, 1))] 