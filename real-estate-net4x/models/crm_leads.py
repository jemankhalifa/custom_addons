from odoo import models, fields, api

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    enquiry_id = fields.Many2one('property.enquiry', string="Related Enquiry")
    property_id = fields.Many2one('property.listing', string="Related Property")
    sales_value = fields.Float(string="Sales Value")
    commission_percentage = fields.Float(string="Commission Percentage")
    commission_amount = fields.Float(string="Commission Amount", compute="_compute_commission_amount", store=True)
    company_share = fields.Float(string="Company Share", compute="_compute_company_share", store=True)
    company_share_percentage = fields.Float(string="Company Share Percentage", default=70)
    agent_share_percentage = fields.Float(string="Agent Share Percentage", default=30)
    agent_share = fields.Float(string="Agent Share", compute="_compute_agent_share", store=True)
    documents = fields.Many2many('ir.attachment', string="Attached Documents")
    product_id = fields.Many2one('product.product', string="Product",related="property_id.product_id")
    @api.depends('sales_value', 'commission_percentage','company_share_percentage')
    def _compute_commission_amount(self):
        for record in self:
            record.commission_amount = (record.sales_value * record.commission_percentage) / 100

    @api.depends('commission_amount','company_share_percentage')
    def _compute_company_share(self):
        for record in self:
            record.company_share = (record.commission_amount * record.company_share_percentage) / 100

    @api.depends('commission_amount','agent_share_percentage')
    def _compute_agent_share(self):
        for record in self:
            record.agent_share = (record.commission_amount * record.agent_share_percentage) / 100

    def _prepare_opportunity_quotation_context(self):
        """ Prepares the context for a new quotation (sale.order) by sharing the values of common fields """
        self.ensure_one()
        quotation_context = {
            'default_opportunity_id': self.id,
            'default_partner_id': self.partner_id.id,
            'default_campaign_id': self.campaign_id.id,
            'default_medium_id': self.medium_id.id,
            'default_origin': self.name,
            'default_source_id': self.source_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_tag_ids': [(6, 0, self.tag_ids.ids)],
            'default_order_line':[(0, 0, {'product_id': self.product_id.id, 'name': self.name, 'product_uom_qty': 1, 'price_unit':self.sales_value})] ,
        }
        if self.team_id:
            quotation_context['default_team_id'] = self.team_id.id
        if self.user_id:
            quotation_context['default_user_id'] = self.user_id.id
        return quotation_context