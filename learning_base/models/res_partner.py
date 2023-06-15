# Copyright 2018 Nicolas JEUDY
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#import barcode
#from barcode.writer import ImageWriter
import base64
import logging
from io import BytesIO
import re
import unicodedata

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # student_barcode = fields.Binary('Barcode', attachment=True, compute="_compute_barcode", store=True)

    is_student = fields.Boolean("Student")
    is_trainer = fields.Boolean("Trainer")
    is_learning_contact = fields.Boolean("Learning contact")
    trainer_cv = fields.Char("CV")
    # ajouter un lien vers linkedin ou site internet

    #@api.depends('ref')
    #def _compute_barcode(self):
    #    for record in self:
    #        if record.ref:
    #            CODE39 = barcode.get_barcode_class('code39')
    #            code39 = CODE39(record.ref, writer=ImageWriter(), add_checksum=False)
    #            fp = BytesIO()
    #            code39.write(fp)
    #            #barcode.generate('code39', self.ref, writer=ImageWriter(), output=fp)
    #            record.student_barcode = base64.b64encode(fp.getvalue())
    #        else:
    #            record.student_barcode = False