# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PropertyListing(models.Model):
    _name = 'property.listing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property Listing'

    name = fields.Char(string="Property Name", required=True,tracking=True)
    location = fields.Char(string="Location",tracking=True)
    product_id = fields.Many2one('product.product', string="Product", tracking=True)
    price = fields.Float(string="Price",tracking=True)
    contact_id = fields.Many2one('res.partner', string="Assigned Contact",tracking=True)
    owner_id = fields.Many2one('res.partner', string="Owner",tracking=True,)
    enquiry_ids = fields.One2many('property.enquiry', 'property_id', string="Enquiries",tracking=True)
    sale_id = fields.Many2one('sale.order', string="Sale",tracking=True)
    status = fields.Selection([('available', 'Available'), ('sold', 'Sold'), ('leased', 'Leased')], string="Status", default='available',tracking=True)
    sales_count = fields.Integer()

    def action_product_create(self):
        self.ensure_one()
        product_id = self.env['product.product'].create({
            'name': self.name,
            'lst_price': self.price,
            'type': 'consu',
            })
        self.product_id = product_id
        self.status = 'available'