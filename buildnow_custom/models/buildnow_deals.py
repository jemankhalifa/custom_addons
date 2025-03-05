# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class BuildnowDeal(models.Model):
    _name = 'buildnow.deal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property Enquiry'

    name = fields.Char(string="Description", required=True)
    transaction_id = fields.Char(string="Transaction ID", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer", tracking=True)
    vendor_id = fields.Many2one('res.partner', related="purchase_id.partner_id",string="Vendor", tracking=True)
    estimate = fields.Many2one('deal.estimate', string="Estimate")
    purchase_id =fields.Many2one('purchase.order', string="Purchase Order")
    sale_id = fields.Many2one('sale.order', string="Sale Order")
    #purchase_status= fields.Selection(related='purchase_id.state', string='Purchase Status')
    rate = fields.Float(string="Rate" ,store=True)
    type = fields.Selection([('deal','Deal'),('third_party','Third Party'),('cash_deal','Cash Deal')], string="Type", default='deal', tracking=True)\

    
class BuildnowEstimate(models.Model):
    _name = 'deal.estimate'

    name = fields.Char(string="Description", required=True)


