from odoo import models, fields, api
from odoo.exceptions import UserError
from num2words import num2words


class AccountPayment(models.Model):
    _inherit = "account.payment"

    check_layout_id = fields.Many2one('check.layout.config', string="Check Layout")

    amount_in_words = fields.Char(string="Amount in Words", compute="_compute_amount_in_words", store=True)

    """Convert Amount in Numbers into Words"""

    @api.depends('amount', 'currency_id')
    def _compute_amount_in_words(self):
        for payment in self:
            if payment.currency_id:
                payment.amount_in_words = num2words(payment.amount, lang='en')
            else:
                payment.amount_in_words = num2words(payment.amount)

    """Overriding Print Check Button to open wizard and Choose from Layouts"""

    def action_print_checks(self):
        return {
            'name': 'Select Check Layout',
            'type': 'ir.actions.act_window',
            'res_model': 'check.layout.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_ids': self.ids},
        }
