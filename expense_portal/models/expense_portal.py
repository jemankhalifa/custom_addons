from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ExpensePortal(models.Model):
    _name = 'expense.portal'
    _description = 'Employee Expense'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee Name', required=True,
                                  default=lambda self: self.env.user.employee_id, readonly=True)
    amount = fields.Float(string='Amount', required=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    note = fields.Text(string='Note')
    state = fields.Selection([
        ('save', 'Save'),
        ('submit', 'Submit To Manager'),
        ('cancel', 'Cancel'),
    ], string='State')

    # definition of validation of amount > 0

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount == 0:
                raise ValidationError('The amount could not be zero!')

    # definition the Buttons of status (save, submit, and cancel)

    def action_save(self):
        for rec in self:
            rec.state = 'save'

    def action_submit(self):
        for rec in self:
            rec.state = 'submit'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

