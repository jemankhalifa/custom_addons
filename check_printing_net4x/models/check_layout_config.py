from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CheckLayoutConfig(models.Model):
    """The check.layout.config model in Odoo is used to store and manage custom check
    layouts for printing checks in the accounting module.
    It allows users to configure the position of check details
    such as check number, date, payee, amount, amount in words, and signature."""

    _name = 'check.layout.config'
    _description = 'Check Layout Configuration'

    name = fields.Char(string="Layout Name", required=True)
    journal_ids = fields.Many2many('account.journal', string="Journals")

    """Padding X,Y Fields (Modify as needed)"""

    check_number_x = fields.Integer(string="Check Number X", default=100)
    check_number_y = fields.Integer(string="Check Number Y", default=50)

    date_x = fields.Integer(string="Date X", default=100)
    date_y = fields.Integer(string="Date Y", default=100)

    payee_x = fields.Integer(string="Payee X", default=100)
    payee_y = fields.Integer(string="Payee Y", default=150)

    amount_x = fields.Integer(string="Amount X", default=100)
    amount_y = fields.Integer(string="Amount Y", default=200)

    amount_words_x = fields.Integer(string="Amount in Words X", default=100)
    amount_words_y = fields.Integer(string="Amount in Words Y", default=250)

    signature_x = fields.Integer(string="Signature X", default=400)
    signature_y = fields.Integer(string="Signature Y", default=300)

    """Page Format Dimensions"""
    page_width = fields.Integer(string='Page Width (mm)')
    page_height = fields.Integer(string='Page Height (mm)')

    @api.constrains('page_width', 'page_height')
    def _check_page_dimensions(self):
        for record in self:
            if record.page_width and record.page_width <= 0:
                raise ValidationError("Page width must be a positive number")
            if record.page_height and record.page_height <= 0:
                raise ValidationError("Page height must be a positive number")

    """Ensure each journal is linked to only one layout."""

    @api.constrains('journal_ids')
    def _check_journal_unique_layout(self):
        for layout in self:
            for journal in layout.journal_ids:
                other_layouts = self.search([('id', '!=', layout.id), ('journal_ids', 'in', journal.id)])
                if other_layouts:
                    raise ValidationError(f"The journal '{journal.name}' is already linked to another layout.")
