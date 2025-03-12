from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class CurrentBalance(models.Model):
    _name = "current.balance.labor"
    _inherit = 'mail.thread'

    name = fields.Char(string='Name', required=True)
    totals = fields.Float(string="Total Amount", compute='_compute_totals', store=True)

    employee_ids = fields.Many2many('hr.employee', 'rel_labor_lines_list', 'current_balance_id', 'employee_id',
                                    string="Employees")
    balance_lines = fields.One2many('current.balance.labor.lines', 'balance_line_id', string="Balance")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    payment_ids = fields.One2many('account.payment', 'balance_sheet_id', string="Payments")
    payment_count = fields.Integer(string='Payment Count', compute='_compute_payment_count')

    @api.depends('payment_ids')
    def _compute_payment_count(self):  # compute the payments for an employee
        for rec in self:
            rec.payment_count = len(rec.payment_ids)

    # Definition of smart button (Payments)
    def action_view_payments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'account.payment',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.payment_ids.ids)],
            'context': {'create': False}
        }

    def compute_balance(self):
        for rec in self:
            rec.balance_lines.unlink()
            for emp in rec.employee_ids:
                invoices = self.env['account.move'].search([('partner_id', '=', emp.user_id.partner_id.id),
                                                            ('state', '=', 'posted'), ('expensed', '=', False),
                                                            ('date', '>=', rec.from_date), ('date', '<=', rec.to_date)])

                expenses = self.env['expense.portal'].search(
                    [('employee_id', '=', emp.id), ('state', '=', 'approved'), ('expensed', '=', False),
                     ('date', '>=', rec.from_date), ('date', '<=', rec.to_date)])
                total_inv = 0
                total_expe = 0
                for invoice in invoices:
                    total_inv += invoice.amount_residual

                for expensed in expenses:
                    total_expe += expensed.amount

                self.env['current.balance.labor.lines'].create({
                    'balance_line_id': rec.id,
                    'employee_id': emp.id,
                    'total_expense_paid': total_expe,
                    'total_work_amount': total_inv,
                    'remaining_balance': total_inv - total_expe
                })

    @api.depends('balance_lines.remaining_balance')
    def _compute_totals(self):
        for rec in self:
            rec.totals = sum(line.remaining_balance for line in rec.balance_lines)

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_pay(self): # when it clicked the pay must be created in payments as vendor payment
        for rec in self:
            journal_id = self.env['account.journal'].search([('type', '=', 'cash')], limit=1)
            if not journal_id:
                raise ValidationError("No cash journal found! Please create a cash journal.")
            payment_list = []
            for line in rec.balance_lines:
                if line.remaining_balance > 0:
                    payment = self.env['account.payment'].create({
                        'partner_id': line.employee_id.user_id.partner_id.id,
                        'payment_type': 'outbound',
                        'amount': line.remaining_balance,
                        'journal_id': journal_id.id,
                        'currency_id': self.env.company.currency_id.id,
                        'payment_method_id': 1,  # Manual payment method
                        'partner_type': 'supplier',
                        'date': fields.Date.today(),
                        'memo': f'Payment for {line.employee_id.name}',
                        'balance_sheet_id': rec.id,
                    })
                    payment_list.append(payment.id)

            rec.write({'payment_ids': [(6, 0, payment_list)]})
            rec.state = 'paid'
    def unlink(self):
        raise UserError("Deleting any record in this form is not allowed.")


class CurrentBalanceLines(models.Model):
    _name = "current.balance.labor.lines"

    balance_line_id = fields.Many2one('current.balance.labor', string="Balance")
    employee_id = fields.Many2one('hr.employee', string="Employees")
    total_expense_paid = fields.Float(string="Total Expenses Paid")
    total_work_amount = fields.Float(string="Total Work Amount")
    remaining_balance = fields.Float(string="Remaining Balance")