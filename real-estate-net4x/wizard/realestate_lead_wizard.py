import base64
import io
import xlsxwriter
from odoo import models, fields, _
from datetime import datetime

class RalestatLeadReportWizard(models.TransientModel):
    _name = 'realestate.lead.report.wizard'
    _description = 'Wizard for Real Estate Leads Excel Report'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    partner_ids = fields.Many2many('res.partner','res_partner_rel','report_id','partner_id', string="Customer")
    state = fields.Selection([
        ('crm.stage_lead1', 'New'),
        ('crm.reale_state_stage_lead1', 'Approved')
    ], string="State", default='crm.stage_lead1')
    xls_file = fields.Binary(string="XLS file")
    xls_filename = fields.Char()

    def action_get_excel_report_data(self):
        # Fetch filtered data based on wizard inputs
        domain = [('is_real_estate_lead', '=', True)]
        # domain = [('is_real_estate_lead', '=', True)]
        if self.partner_ids:
            domain.append(('create_date', '>=', self.start_date))
        if self.partner_ids:
            domain.append(('create_date', '<=', self.end_date))
        if self.partner_ids:
            domain.append(('partner_id', 'in', self.partner_ids.ids))
        if self.state:
            stage = self.state
            stage_id = self.env.ref(stage).id
            domain.append(('stage_id', '=', stage_id))

        realestate_leads = self.env['crm.lead'].search(domain)
        return realestate_leads

    def action_generate_excel_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Real Estate Leads")
        bold = workbook.add_format({'bold': True})
        leads = self.action_get_excel_report_data()
        # Write headers
        sheet.write(0, 0, 'lead Date', bold)
        sheet.write(0, 1, 'Customer', bold)
        sheet.write(0, 2, 'Opportunity Name', bold)
        sheet.write(0, 3, 'Property Name', bold)
        sheet.write(0, 4, 'Total Amount', bold)
        sheet.write(0, 5, 'State', bold)

        # Write data rows
        row = 1
        for lead in leads:
            sheet.write(row, 0, str(lead.create_date.date()))
            sheet.write(row, 1, lead.partner_id.name)
            sheet.write(row, 2, lead.name)
            sheet.write(row, 3, lead.property_id.name)
            sheet.write(row, 4, lead.commission_amount)
            sheet.write(row, 5, lead.stage_id.name)
            row += 1

        workbook.close()


        attachment_id = self.env['ir.attachment'].create({
            'name': f"{self.display_name} - {_('Real Estate Report')}",
            'datas': base64.encodebytes(output.getvalue())
        })
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment_id.id}",
            "target": "download",
        }