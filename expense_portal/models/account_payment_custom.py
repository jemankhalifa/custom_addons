from odoo import models, fields, api


class AccountPaymentCustom(models.Model):
    _inherit = 'account.payment'

    balance_sheet_id = fields.Many2one('current.balance.labor', string="Balance Sheet")
