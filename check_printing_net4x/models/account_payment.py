from odoo import models, fields, api
from odoo.exceptions import UserError
from num2words import num2words


class AccountPayment(models.Model):
    _inherit = "account.payment"

    check_layout_id = fields.Many2one('check.layout.config', string="Check Layout")

    amount_in_words = fields.Char(string="Amount in Words", compute="_compute_amount_in_words",
                                  store=True)

    """Convert Amount in Numbers into Words"""

    @api.depends('amount', 'currency_id')
    def _compute_amount_in_words(self):
        for payment in self:
            if payment.currency_id:
                payment.amount_in_words = num2words(payment.amount, lang='en')
            else:
                payment.amount_in_words = num2words(payment.amount)

    """Triggers the check printing report with the selected layout."""

    def _print_check(self, layout):
        return self.env.ref('check_printing_net4x.report_check_printing').report_action(
            self.ids,
            data={
                'layout_id': layout.id,
                'docids': self.ids
            }
        )

    """If the journal has a linked layout, print directly, otherwise open the wizard"""

    def action_print_checks(self):
        self.ensure_one()

        # 1. Check journal's direct layout link
        if self.journal_id.check_layout_id:
            return self._print_check(self.journal_id.check_layout_id)

        # 2. Check for any layout linked through journal_ids
        check_layout = self.env['check.layout.config'].search([
            ('journal_ids', 'in', self.journal_id.id)
        ], limit=1)

        if check_layout:
            return self._print_check(check_layout)

        # 3. If no layout found, open wizard
        return {
            'name': 'Select Check Layout',
            'type': 'ir.actions.act_window',
            'res_model': 'check.layout.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_payment_id': self.id,
                'default_journal_id': self.journal_id.id,
                'active_ids': self.ids,
            },
        }
