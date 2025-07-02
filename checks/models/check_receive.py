from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import AccessError


class CheckReceive(models.Model):
    _name = 'check.receive'
    _description = 'Check Receive Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Check Number', required=True, tracking=True)
    beneficiary = fields.Char(string='Beneficiary', required=True, tracking=True)
    bank_id = fields.Many2one('res.bank', string='Bank', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    amount = fields.Float(string='Amount', required=True, tracking=True)
    payment_id = fields.Many2one('account.payment', string='Related Payment')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('received', 'Received'),
        ('deposited', 'Deposited'),
        ('cleared', 'Cleared'),
        ('bounced', 'Bounced'),
    ], string='Status', default='draft', tracking=True)
    check_image = fields.Binary(string='Check Image')
    note = fields.Text(string='Notes')

    reconciliation_status = fields.Selection([
        ('not_reconciled', 'Not Reconciled'),
        ('reconciled', 'Reconciled')
    ], string='Reconciliation Status', default='not_reconciled', tracking=True)

    statement_line_id = fields.Many2one('account.bank.statement.line', string='Bank Statement Line')
    reconciliation_notes = fields.Text(string='Reconciliation Notes')

    @api.model
    def _cron_check_due_reminder(self):
        today = fields.Date.today()
        upcoming = self.search([
            ('date', '<=', today)
        ])
        for check in upcoming:
            check.message_post(
                body=_("Reminder: This check is due today or overdue!"),
                message_type='notification'
            )

    def action_set_received(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Check can only be sent from Issued status.'))
            record.state = 'received'

    def action_set_deposited(self):
        for record in self:
            if record.state != 'received':
                raise UserError(_('Check can only be sent from Issued status.'))
            record.state = 'deposited'

    def action_set_cleared(self):
        for record in self:
            if record.state != 'deposited':
                raise UserError(_('Check can only be sent from Issued status.'))
            record.state = 'cleared'

    def action_set_bounced(self):
        for record in self:
            if record.state != 'cleared':
                raise UserError(_('Check can only be sent from Issued status.'))
            record.state = 'bounced'

    def print_check_report(self):
        return self.env.ref('checks.action_checkreceive_report').report_action(self)

    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Cannot delete a check that is not in Draft status.'))
        return super(CheckReceive, self).unlink()

    def action_mark_as_reconciled(self):
        for record in self:
            record.reconciliation_status = 'reconciled'
            record.message_post(body=_("Marked as Reconciled"))

    def write(self, vals):
        for rec in self:
            if not self.env.user.has_group('checks.group_check_receive_finance_manager'):
                raise AccessError(_("You do not have permission to modify this record."))
        return super(CheckReceive, self).write(vals)

    def action_mark_as_reconciled(self):
        if not self.env.user.has_group('checks.group_check_receive_finance_manager'):
            raise AccessError(_("You do not have permission to reconcile this check."))
        self.reconciliation_status = 'reconciled'
        self.message_post(body=_("Marked as Reconciled"))
