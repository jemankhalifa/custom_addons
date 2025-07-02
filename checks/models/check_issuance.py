from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CheckIssuance(models.Model):
    _name = 'check.issuance'
    _description = 'Check Issuance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Check Number', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    beneficiary = fields.Char(string='Beneficiary', required=True, tracking=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    amount = fields.Float(string='Amount', required=True, tracking=True)
    bank_id = fields.Many2one('res.bank', string='Bank', required=True)
    bank_account_id = fields.Many2one('account.account', string='Bank Account', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('sent', 'Sent'),
    ], string='Status', default='draft', tracking=True)
    attachment_ids = fields.One2many('ir.attachment', 'res_id', string='Attachments',
                                     domain=[('res_model', '=', 'check.issuance')])
    note = fields.Text(string='Notes')
    attachment_count = fields.Integer(string='Attachments', compute='_compute_attachment_count')
    payment_count = fields.Integer(string='Payment Count', compute='_compute_payment_count')
    statement_count = fields.Integer(string='Bank Statement Count', compute='_compute_statement_count')

    @api.depends()
    def _compute_statement_count(self):
        for record in self:
            record.statement_count = self.env['account.bank.statement.line'].search_count([
                ('name', '=', record.name)
            ])

    @api.depends()
    def _compute_payment_count(self):
        for record in self:
            record.payment_count = self.env['account.payment'].search_count([
                ('check_number', '=', record.name)
            ])

    @api.depends('attachment_ids')
    def _compute_attachment_count(self):
        for record in self:
            record.attachment_count = len(record.attachment_ids)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('check.issuance') or _('New')
        return super(CheckIssuance, self).create(vals)

    def action_issue_check(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Check can only be issued from Draft status.'))
            record.state = 'issued'

    def action_send_check(self):
        for record in self:
            if record.state != 'issued':
                raise UserError(_('Check can only be sent from Issued status.'))
            record.state = 'sent'

    def print_check_report(self):
        return self.env.ref('checks.action_checkissuance_report').report_action(self)

    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Cannot delete a check that is not in Draft status.'))
        return super(CheckIssuance, self).unlink()

    def action_open_attachments(self):
        self.ensure_one()
        return {
            'name': _('Attachments'),
            'type': 'ir.actions.act_window',
            'res_model': 'ir.attachment',
            'view_mode': 'list,form',
            'domain': [
                ('res_model', '=', self._name),
                ('res_id', '=', self.id)
            ],
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id,
            }
        }

    def action_view_payments(self):
        self.ensure_one()
        return {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_mode': 'list,form',
            'domain': [('check_number', '=', self.name)],
            'context': {'create': False},

        }

    def action_view_bank_statements(self):
        self.ensure_one()
        return {
            'name': _('Bank Statements'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.bank.statement.line',
            'view_mode': 'list,form',
            'domain': [('name', '=', self.name)],
            'context': {'create': False},
        }
