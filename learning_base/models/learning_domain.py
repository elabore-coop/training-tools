from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LearningDomain(models.Model):
    _name = 'learning.domain'
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char('Name')
    code = fields.Char('Code', translate=False)
    parent_id = fields.Many2one('learning.domain', 'Parent Domain', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_id = fields.One2many('learning.domain', 'parent_id', 'Child Domain')

    @api.constrains('parent_id')
    def _check_domain_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive domain.'))
        return True