from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class CustomerInstallments(models.Model):
    _name = 'customer.installments'
    _description = 'Customer Installments Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    product = fields.Many2one('product.product', string="Product", required=True, tracking=True)
    start_date = fields.Date(string="Start Date", required=True)
    total_amount = fields.Float(string="Total Amount", required=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    installment_count = fields.Integer(string="Installment Count", required=True, tracking=True)
    description = fields.Text(string="Description")
    Installment_type = fields.Selection([('weekly', 'Weekly'),
                                         ('monthly', 'Monthly'),
                                         ('annually', 'Annually')], string="Installment Type",
                                        required=True, tracking=True)
    installment_ids = fields.One2many('deposit.installments', 'deposit_id', string='Installments')

    # Generating Installments Button Definition
    def generate_installments(self):
        self.ensure_one()
        installment_amount = self.total_amount / self.installment_count
        date = self.start_date

        self.installment_ids.unlink()

        for _ in range(self.installment_count):
            self.env['deposit.installments'].create({
                'deposit_id': self.id,
                'amount': installment_amount,
                'due_date': date,
                'state': 'pending'
            })

            if self.Installment_type == 'weekly':
                date += relativedelta(weeks=1)
            elif self.Installment_type == 'monthly':
                date += relativedelta(months=1)
            elif self.Installment_type == 'annually':
                date += relativedelta(years=1)
