# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class PropertyEnquiry(models.Model):
    _name = 'property.enquiry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property Enquiry'

    name = fields.Char(string="Description", required=True)
    status = fields.Selection([
        ('untouched', 'Untouched'),
        ('touched', 'Touched'),
        ('not_serious', 'Not Serious')
    ], string="Status", default='untouched', required=True,tracking=True)
    contact_id = fields.Many2one('res.partner', string="Contact",tracking=True)
    property_id = fields.Many2one('property.listing', string="Property",tracking=True)
    opportunity_id = fields.Many2one('crm.lead', string="Opportunity",tracking=True)
    contact_name = fields.Char(string="Contact Name",tracking=True)
    contact_phone = fields.Char(string="Contact Phone",tracking=True)
    contact_email = fields.Char(string="Contact Email",tracking=True)
    note = fields.Text(string="Note")
    product_id = fields.Many2one('product.product', string="Product", related="property_id.product_id")
    contacts_count = fields.Integer()

    def action_oppourtinity_create(self):
        if not (self.contact_name or self.contact_phone or  self.contact_email):
           raise UserError("Please fill at least Name, phone or an email before create an oppourtinity.")
        
        if not (self.property_id):
           raise UserError("Please add select the property before create an oppourtinity.")
        self.action_contact_create()
        opportunity_id = self.env["crm.lead"].create({
            'name': self.name,
            'partner_id': self.contact_id.id,
            'enquiry_id': self.id,
            'property_id': self.property_id.id,
            'product_id':self.product_id.id,
            'sales_value': self.property_id.price
        })
        self.opportunity_id = opportunity_id
        self.contact_id.property_ids=[self.property_id.id]
        self.status = 'touched'
        
    def action_contact_create(self):
       if not (self.contact_name or self.contact_phone or  self.contact_email):
           raise UserError("Please fill at least Name, phone or an email before create a contact.")
           
       contact_id= self.env["res.partner"].create({
            'name': self.contact_name,
            'phone': self.contact_phone,
            'email': self.contact_email,
            'type': 'contact',
        })
       self.contact_id = contact_id
       self.contact_id.enquiry_ids=[self.id]
       self.status = 'touched'


    def action_show_contact(self):
        self.ensure_one()
        return {
            'name': 'Contact Details',
            'view_type': 'form',
            'view_mode': 'form',
           'res_model':'res.partner',
            'res_id': self.contact_id.id,
            'context': {'default_enquiry_id': self.id},
        }
