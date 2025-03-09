from odoo import models, fields, api
from odoo.exceptions import ValidationError



class ExpensePortal(models.Model):
    _name = 'expense.portal'
    _description = 'Employee Expense Portal'
    _inherit = 'mail.thread'

    name = fields.Char(compute="set_name_value",string="Name")
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True,
                                  default=lambda self: self.env.user.employee_id)
    amount = fields.Monetary(string='Amount', required=True, default=0.0)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=False,default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', 'Currency', related='company_id.currency_id', readonly=True, required=True)
    date = fields.Date(string='Date', default=fields.Date.today())
    note = fields.Text(string='Note')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted To Manager'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft')

    payment_id = fields.Many2one('account.payment', string="Payment")
    expensed = fields.Boolean(string="Expensed?")

    payment_count = fields.Integer(string="Payment Count", compute="_compute_payment_count")

    @api.depends('employee_id')
    def set_name_value(self):
        for rec in self:
            rec.name = f'{rec.employee_id.name} - {rec.date}'

    # definition of validation of amount > 0
    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount == 0:
                raise ValidationError('The amount could not be zero!')

    def action_save(self):
        """Save the expense as a draft."""
        self.write({'state': 'draft'})
    
    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_reject(self):
        """Save the expense as a draft."""
        self.write({'state': 'rejected'})

    def action_approve(self):
        """Submit the expense to the manager and create a corresponding record in hr.expense."""
        journal_id = self.env['account.journal'].search([('type','=','cash')])[0]
        for rec in self:
            # Create a record in the hr.expense model
            payment = self.env['account.payment'].create({
                'partner_id': rec.employee_id.user_id.partner_id.id,
                'payment_type': 'inbound',
                'amount': rec.amount,
                'journal_id': journal_id.id,
                'currency_id': rec.currency_id.id,
                'payment_method_id': 1,  # Manual payment method
                'partner_type':'customer',
                'date': rec.date,
                'memo': rec.note,
            })

            # Link the portal expense to the hr.expense record
            rec.write({'state': 'approved'})
            rec.payment_id = payment

    def action_cancel(self):
        """Cancel the expense."""
        self.write({'state': 'cancelled'})

    def _compute_payment_count(self):
        for rec in self:
            rec.payment_count = self.env['account.payment'].search_count([('id', '=', rec.payment_id.id)])

    def action_view_payments(self):
        self.ensure_one()
        domain = [('id', '=', self.payment_id.id)] if self.payment_id else []
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'account.payment',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {'create': False},
        }
