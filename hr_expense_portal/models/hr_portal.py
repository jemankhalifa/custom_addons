class HrEmployee(models.Model):
    _inherit = 'expense.portal'

    def get_remaining_balance(self):
        self.ensure_one()
        total_inv = 0
        total_expe = 0

        invoices = self.env['account.move'].search([
            ('partner_id', '=', self.user_id.partner_id.id),
            ('state', '=', 'posted'),
            ('expensed', '=', False),
        ])
        expenses = self.env['expense.portal'].search([
            ('employee_id', '=', self.id),
            ('state', '=', 'approved'),
            ('expensed', '=', False),
        ])

        for invoice in invoices:
            total_inv += invoice.amount_residual

        for exp in expenses:
            total_expe += exp.amount

        return total_inv - total_expe
