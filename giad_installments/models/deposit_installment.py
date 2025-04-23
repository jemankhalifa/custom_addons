from odoo import models, fields, api


class DepositInstallment(models.Model):
    _name = 'deposit.installments'
    _description = 'Installment Payment'

    deposit_id = fields.Many2one('customer.installments', ondelete='cascade')
    amount = fields.Float(string='Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    due_date = fields.Date(required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid')
    ], default='pending')

    # Creating Customer Payment
    @api.model
    def check_due_and_pay(self):
        today = fields.Date.today()
        for installment in self.search([('state', '=', 'pending'), ('due_date', '<=', today)]):
            # Simulate payment
            self.env['account.payment'].create({
                'payment_type': 'outbound',
                'partner_type': 'supplier',
                'partner_id': installment.deposit_id.partner_id.id,
                'amount': installment.amount,
                'payment_method_id': self.env.ref('account.account_payment_method_manual_out').id,
                'journal_id': self.env['account.journal'].search([('type', '=', 'bank')], limit=1).id,
            }).action_post()
            installment.state = 'paid'
