# Copyright 2018 Nicolas JEUDY
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class learningFinancialProgram(models.Model):
    _name = 'learning.financial.program'
    _description = "Learning Financial Program"

    product_tmpl_ids = fields.Many2many('product.template', 'financial_program_product_category_rel',  'financial_program_id',  'product_category_id', 'Products')
    name = fields.Char("Name")
    description = fields.Text('Description')
    description_html = fields.Html("Web Description")


class ProductTemplate(models.Model):
    _inherit = ['product.template']

    is_learning = fields.Boolean(compute='_compute_is_learning')
    detailed_type = fields.Selection(selection_add=[
        ('learning', 'Training'),
    ], ondelete={'learning': 'set service'})
    
    
    goal = fields.Html(string='Goal', translate=True)
    duration_html = fields.Html(string='Duration', translate=True)
    public = fields.Html(string='Public', translate=True)
    prerequisite = fields.Html(string='Prerequisite', translate=True)
    content = fields.Html(string='Content', translate=True)
    organizer = fields.Html(string='Organizer', translate=True)
    methodology = fields.Html(string='Methodology', translate=True)
    technic = fields.Html(string='Technical', translate=True)
    price_html = fields.Html(string='Price', translate=True)
    registration = fields.Html(string='Registration', translate=True)
    
    our_value = fields.Html(string='Value', translate=True)

    description = fields.Html(string='Description', translate=True)
    validate = fields.Html(string='Validate', translate=True)
    certificate = fields.Html(string='Certificate', translate=True)
    
    financial_program_ids = fields.Many2many('learning.financial.program', 'financial_program_product_category_rel',  'product_category_id', 'financial_program_id', 'Financial Program')
    parent_domain_id = fields.Many2one('learning.domain',  related='domain_id.parent_id', store=True, string="Domain parent")
    domain_id = fields.Many2one('learning.domain', string="Domain")
    duration_hour = fields.Float('Duration in hour(s)')
    hours_per_day = fields.Float('Nb hour(s) per day(s) ?')
    duration_days = fields.Float('Duration in day(s)')
    duration_text = fields.Text('Duration details')
    count_session = fields.Integer('Nb session', compute="_compute_session", readonly=True)
    sessions_ids = fields.One2many('event.event', 'learning_id', 'Slots')

    # ajouter la nature de l'action de formation avec la liste

    def _compute_session(self):
        for record in self:
            record.count_session = len(self.env['event.event'].search([('learning_id', '=', record.id)]))

    @api.depends('detailed_type')
    def _compute_is_learning(self):
        for record in self:
            record.is_learning = record.detailed_type == 'learning'

    