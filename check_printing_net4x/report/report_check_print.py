from odoo import models, fields, api


class ReportCheckPrint(models.AbstractModel):
    _name = 'report.check_printing_net4x.report_check_template'
    _description = 'Check Printing Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.payment'].browse(docids)
        layout_id = data.get('layout_id') if data else None
        layout = self.env['check.layout.config'].browse(layout_id) if layout_id else None

        return {
            'docs': docs,
            'layout': layout,  # Pass the selected layout to the template
        }
