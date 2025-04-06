from odoo import models, fields, api
from odoo.exceptions import UserError


class CheckLayoutWizard(models.TransientModel):
    _name = 'check.layout.wizard'
    _description = 'Check Layout Selection Wizard'

    layout_id = fields.Many2one('check.layout.config', string="Check Layout", required=True)

    """Trigger check printing with selected layout"""

    def action_print_check(self):
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            raise UserError("No payments selected for printing!")

        return self.env.ref('check_printing_net4x.report_check_printing').report_action(
            active_ids,
            data={
                'layout_id': self.layout_id.id,
                'docids': active_ids
            }
        )
