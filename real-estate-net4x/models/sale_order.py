from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # is_property_lead = fields.Boolean(related='opportunity_id.is_property_lead')
    # approved_property_lead = fields.Boolean(related='opportunity_id.approved_property_lead')
    is_real_estate_lead = fields.Boolean(string="Real Estate Lead?")
    # approved_real_estate_lead = fields.Boolean(related='opportunity_id.approved_real_estate_lead')
    # # enquiry_id = fields.Many2one('property.enquiry', string="Related Enquiry")
    # # property_id = fields.Many2one('property.listing', string="Property")
    # sales_value = fields.Float(related='opportunity_id.sales_value')
    # commission_percentage = fields.Float(related='opportunity_id.commission_percentage')
    # commission_amount = fields.Float(related='opportunity_id.commission_amount')
    # company_share = fields.Float(related='opportunity_id.company_share')
    # company_share_percentage = fields.Float(related='opportunity_id.company_share_percentage')
    # referal_agent_percentage = fields.Float(related='opportunity_id.referal_agent_percentage')
    # referal_agent_share = fields.Float(related='opportunity_id.referal_agent_share')
    # agent_share_percentage = fields.Float(related='opportunity_id.agent_share_percentage')
    # agent_share = fields.Float(related='opportunity_id.agent_share')
    # # documents = fields.Many2many(related='opportunity_id.documents')
    # # product_id = fields.Many2one(related='opportunity_id.product_id'")
    # agent_id = fields.Many2one(related='opportunity_id.agent_id')
