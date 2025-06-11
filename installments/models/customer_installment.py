from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class CustomerInstallments(models.Model):
    _name = 'customer.installments'
    _description = 'Customer Installments Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    reference = fields.Char(string="Reference", default=lambda self: _('New'), readonly=True, copy=False)
    product = fields.Many2one('product.product', string="Product", required=True, tracking=True)
    start_date = fields.Date(string="Start Date", required=True)
    total_amount = fields.Float(string="Total Amount", required=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    installment_count = fields.Integer(string="Installment Count", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    installment_type = fields.Selection([('weekly', 'Weekly'),
                                         ('monthly', 'Monthly'),
                                         ('annually', 'Annually')],
                                        string="Installment Type",
                                        required=True, tracking=True)

    state = fields.Selection([('draft', 'Draft'),
                              ('in_progress', 'In Progress'),
                              ('paid', 'Paid')], string="Status", default="draft", tracking=True)

    installment_ids = fields.One2many('deposit.installments', 'deposit_id', string='Installments')
    payment_progress = fields.Float(string="Payment Progress", compute="_compute_payment_progress", store=False)

    def action_confirm(self):
        for rec in self:
            rec.state = 'in_progress'

    # Automatically generate a reference number for installments

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('customer.installments')
        return super(CustomerInstallments, self).create(vals)

    # Generating Installments Button Definition

    def generate_installments(self):
        self.ensure_one()
        installment_amount = self.total_amount / self.installment_count
        date = self.start_date

        self.installment_ids.unlink()

        payment_method = self.env.ref('account.account_payment_method_manual_in', raise_if_not_found=False)
        journal = self.env['account.journal'].search([('type', '=', 'bank')], limit=1)

        for i in range(self.installment_count):
            installment = self.env['deposit.installments'].create({
                'deposit_id': self.id,
                'partner_id': self.partner_id.id,
                'amount': installment_amount,
                'due_date': date,
            })

            # Create a customer payment linked to the installment
            payment = self.env['account.payment'].create({
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'partner_id': self.partner_id.id,
                'amount': installment_amount,
                'date': date,
                'currency_id': self.currency_id.id,
                'payment_method_id': payment_method.id,
                'journal_id': journal.id,
                'memo': f"Installment {self.reference} ({i + 1}/{self.installment_count})",
            })

            payment.action_post()

            # Link payment to the installment
            installment.payment_id = payment.id

            # Move to next due date
            if self.installment_type == 'weekly':
                date += relativedelta(weeks=1)
            elif self.installment_type == 'monthly':
                date += relativedelta(months=1)
            elif self.installment_type == 'annually':
                date += relativedelta(years=1)

    @api.depends('installment_ids.payment_id.state')
    def _compute_payment_progress(self):
        for record in self:
            total = len(record.installment_ids)
            paid = len(record.installment_ids.filtered(lambda r: r.payment_id and r.payment_id.state == 'paid'))
            if total > 0:
                record.payment_progress = (paid / total) * 100
            else:
                record.payment_progress = 0.0
