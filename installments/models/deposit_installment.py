from odoo import models, fields, api
from odoo.exceptions import UserError


class DepositInstallment(models.Model):
    _name = 'deposit.installments'
    _description = 'Installment Payment'

    deposit_id = fields.Many2one('customer.installments', ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Customer')
    amount = fields.Float(string='Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    due_date = fields.Date(required=True)
    state = fields.Selection(related='payment_id.state', store=True, readonly=True)
    payment_id = fields.Many2one('account.payment', string='Payment', readonly=True)

    @api.constrains('state')
    def update_general_state(self):
        for rec in self:
            all_paid = all([s == 'paid' for s in rec.deposit_id.installment_ids.mapped('state')])
            if all_paid:
                rec.deposit_id.state = 'paid'
            else:
                if rec.deposit_id.state == 'paid':
                    rec.deposit_id.state = 'in_progress'

    # Creating Customer Payment
    @api.model
    def check_due_and_pay(self):
        today = fields.Date.today()
        for installment in self.search([('state', '=', 'pending'), ('due_date', '<=', today)]):
            self.env['account.payment'].create({
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'partner_id': installment.deposit_id.partner_id.id,
                'amount': installment.amount,
                'payment_method_id': self.env.ref('account.account_payment_method_manual_out').id,
                'journal_id': self.env['account.journal'].search([('type', '=', 'bank')], limit=1).id,
            }).action_post()
            installment.state = 'paid'


    # Smart Button to Redirect to Payment
    def action_view_payment(self):
        self.ensure_one()
        if not self.payment_id:
            raise UserError("No payment linked to this installment.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Payment',
            'res_model': 'account.payment',
            'view_mode': 'form',
            'res_id': self.payment_id.id,
            'target': 'current',
        }
