from odoo import models, fields, api


class ReportCheckPrint(models.AbstractModel):
    _name = 'report.check_printing_net4x.report_check_template'
    _description = 'Check Printing Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Get effective docids from context or data
        effective_docids = data.get('docids', docids) if data else docids
        docs = self.env['account.payment'].browse(effective_docids)

        # Get layout from data (passed from wizard or context)
        layout = self.env['check.layout.config'].browse(data.get('layout_id')) if data else None

        return {
            'doc_ids': effective_docids,
            'doc_model': 'account.payment',
            'docs': docs,
            'layout': layout,
        }
