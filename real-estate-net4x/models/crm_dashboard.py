from odoo import models, fields, api

class CRMLead(models.Model):
    _name = 'crm.lead.dashboard'
    
    total_inquiries = fields.Integer(string='Total Inquiries', compute='_compute_total_inquiries')
    total_listings = fields.Integer(string='Total Listings', compute='_compute_total_listings')
    total_commissions = fields.Float(string='Total Commissions', compute='_compute_total_commissions')

    @api.depends()
    def _compute_total_inquiries(self):
        enquires = self.env['property.enquiry'].search([])
        self.total_inquiries = len(enquires)

    @api.depends()
    def _compute_total_listings(self):
        listing = self.env['property.listing'].search([])
        self.total_listings = len(listing)

    @api.depends()
    def _compute_total_commissions(self):
        leads = self.env['crm.lead'].search([])
        for record in leads:
            commissions += record.company_share
            #record.total_commissions = commissions
