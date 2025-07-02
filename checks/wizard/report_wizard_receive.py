from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CheckReportWizard(models.TransientModel):
    _name = 'check.report.wizard'
    _description = 'Wizard to generate check report'

    date_from = fields.Date(string="From Date", required=True)
    date_to = fields.Date(string="To Date", required=True)

    def action_print_check_receive(self):
            data = {
                'form': self.read()[0],
            }
            return self.env.ref('checks.action_check_report_pdf').report_action(self, data=data)

   