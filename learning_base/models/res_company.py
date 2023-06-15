# Copyright 2018 Nicolas JEUDY
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    learning_code = fields.Char('Learning Code')
    learning_support_email = fields.Char("Support Email")