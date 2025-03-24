from odoo import models, fields


class CheckLayoutConfig(models.Model):
    """The check.layout.config model in Odoo is used to store and manage custom check
    layouts for printing checks in the accounting module.
    It allows users to configure the position of check details
    such as check number, date, payee, amount, amount in words, and signature."""

    _name = 'check.layout.config'
    _description = 'Check Layout Configuration'

    name = fields.Char(string="Layout Name", required=True)
    journal_id = fields.Many2one('account.journal', string="Bank Journal", required=True)


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



    """Page Width & Height"""
    page_width = fields.Integer(string='Page Width')
    page_height = fields.Integer(string='Page Height')