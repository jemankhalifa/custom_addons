from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    enquiry_ids = fields.One2many('property.enquiry', 'contact_id', string="Enquiries")
    property_ids = fields.One2many('property.listing', 'contact_id', string="Properties")
