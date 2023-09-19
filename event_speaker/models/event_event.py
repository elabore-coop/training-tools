# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    speakers = fields.Many2many(
        'res.partner', string="Speakers"
    )
