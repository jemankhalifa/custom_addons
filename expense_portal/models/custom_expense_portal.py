from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ExpensePortal(models.Model):
    _name = 'expense.portal'
    _description = 'Employee Expense Portal'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True,
                                  default=lambda self: self.env.user.employee_id)
    amount = fields.Float(string='Amount', required=True, default=0.0)
    date = fields.Date(string='Date', default=fields.Date.today())
    note = fields.Text(string='Note')
    state = fields.Selection([
        ('draft', 'Save'),
        ('submitted', 'Submitted To Manager'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft')
    expense_id = fields.Many2one('hr.expense', string='Linked Expense', readonly=True)

    # definition of validation of amount > 0
    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount == 0:
                raise ValidationError('The amount could not be zero!')

    def action_save(self):
        """Save the expense as a draft."""
        self.write({'status': 'draft'})

    def action_submit(self):
        """Submit the expense to the manager and create a corresponding record in hr.expense."""
        for rec in self:
            # Create a record in the hr.expense model
            expense = self.env['hr.expense'].create({
                'employee_id': rec.employee_id.id,
                'name': f"Expense by {rec.employee_id.name}",
                'product_id': self.env.ref('hr_expense.product_product_no_cost').id,
                'unit_amount': rec.amount,
                'date': rec.date,
                'description': rec.note,
            })

            # Link the portal expense to the hr.expense record
            rec.write({'expense_id': expense.id, 'state': 'submitted'})

            # Call the submit_to_manager method from the hr.expense model
            expense.action_submit_expenses()

            # Call the create_report method from the hr.expense model
            expense.action_create_report()

    def action_cancel(self):
        """Cancel the expense."""
        self.write({'state': 'cancelled'})