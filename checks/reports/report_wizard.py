from odoo import api, models, _
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


# Receive Report Wizard

class ReportCheckWizardPDF(models.AbstractModel):
    _name = 'report.checks.report_check_report_pdf'
    _description = 'Check Report Wizard PDF'

    @api.model
    def _get_report_values(self, docids, data):
        if not data or 'form' not in data:
            _logger.error("No data or form in report")
            return {}

        form_data = data['form']
        date_from = form_data.get('date_from')
        date_to = form_data.get('date_to')
        domain = []
        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))

        checks_in = self.env['check.receive'].search(domain)

        _logger.warning("Found checks_in: %s", checks_in)

        return {
            'doc_ids': docids,
            'doc_model': 'check.report.wizard',
            'docs': self.env['check.report.wizard'].browse(docids),
            'checks_in': checks_in,
        }


# Issuance Report Wizard

class ReportCheckIssuanceWizardPDF(models.AbstractModel):
    _name = 'report.checks.report_checkissuance_report_pdf'
    _description = 'Check Issuance Report Wizard PDF'

    @api.model
    def _get_report_values(self, docids, data):
        if not data or 'form' not in data:
            _logger.error("No data or form in report")
            return {}

        form_data = data['form']
        date_from = form_data.get('date_from')
        date_to = form_data.get('date_to')
        domain = []
        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))
        checks_out = self.env['check.issuance'].search(domain)

        _logger.warning("Found checks_out: %s", checks_out)

        return {
            'doc_ids': docids,
            'doc_model': 'check.report.wizard',
            'docs': self.env['check.report.wizard'].browse(docids),
            'checks_out': checks_out,
        }
