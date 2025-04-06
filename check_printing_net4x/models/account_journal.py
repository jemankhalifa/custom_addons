from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    check_layout_id = fields.Many2one('check.layout.config', string="Check Layout")
