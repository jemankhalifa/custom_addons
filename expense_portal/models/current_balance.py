from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CurrentBalance(models.Model):
    _name = "current.balance.labor"

    name = fields.Char(string='Name', required=True)
    totals = fields.Float(string="Total Amount")
    employee_ids = fields.Many2many('hr.employee','rel_labor_lines_list','current_balance_id','employee_id',  string="Employees")
    balance_lines = fields.One2many('current.balance.labor.lines','balance_line_id' ,string="Balance")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    def compute_balance(self):
        for rec in self:
            for emp in rec.employee_ids:
                invoices = self.env['account.move'].search([('partner_id','=',emp.user_id.partner_id.id),
                                                            ('state','=','posted'),('expensed','=',False),
                                                            ('date','>=', rec.from_date), ('date','<=', rec.to_date)])
                
                expenses = self.env['expense.portal'].search([('employee_id','=',emp.id),('state','=','approved'),('expensed','=',False),
                                                            ('date','>=', rec.from_date), ('date','<=', rec.to_date)])
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
          
class CurrentBalanceLines(models.Model):
    _name = "current.balance.labor.lines"

    balance_line_id = fields.Many2one('current.balance.labor', string="Balance")
    employee_id  = fields.Many2one('hr.employee', string="Employees")
    total_expense_paid = fields.Float(string="Total Expenses Paid")
    total_work_amount = fields.Float(string="Total Work Amount")
    remaining_balance = fields.Float(string="Remaining Balance")