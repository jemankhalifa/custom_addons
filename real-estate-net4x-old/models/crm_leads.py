from odoo import models, fields, api

class Lead(models.Model):
    _inherit = 'crm.lead'

    # is_property_lead = fields.Boolean(string="Real Estate Lead?")
    # approved_property_lead = fields.Boolean(string="Approved Real Estate Lead?")
    is_real_estate_lead = fields.Boolean(string="Real Estate Lead?")
    approved_real_estate_lead = fields.Boolean(string="Approved Real Estate Lead?")
    sales_value = fields.Float(string="Sales Value")
    commission_percentage = fields.Float(string="Commission Percentage")
    commission_amount = fields.Float(string="Commission Amount", compute="_compute_commission_amount", store=True)
    company_share = fields.Float(string="Company Share", compute="_compute_company_share", store=True)
    company_share_percentage = fields.Float(string="Company Share Percentage", default=70)
    referal_agent_percentage = fields.Float(string="Referal Agent Percentage")
    referal_agent_share = fields.Float(string="Referal Agent Share", compute="_compute_referal_agent_share", store=True)
    agent_share_percentage = fields.Float(string="Agent Share Percentage", default=30)
    agent_share = fields.Float(string="Agent Share", compute="_compute_agent_share", store=True)
    documents = fields.Many2many('ir.attachment', string="Attached Documents")
    # product_id = fields.Many2one('product.product', string="Product",related="property_id.product_id")
    agent_id = fields.Many2one('res.partner', string="Agent")
    property_id = fields.Many2one('account.analytic.account', string="Property")
    
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

    @api.depends('commission_amount','referal_agent_percentage')
    def _compute_referal_agent_share(self):
        for record in self:
            record.referal_agent_share = (record.commission_amount * record.referal_agent_percentage) / 100


    # @api.depends('commission_amount','agent_share_percentage')
    def action_approve_real_estate_lead(self):
        for record in self:
            record.stage_id = self.env.ref('crm.reale_state_stage_lead1')
            record.approved_real_estate_lead = True

    def action_real_estate_quotations_new(self):
    #     if not self.partner_id:
    #         return self.env["ir.actions.actions"]._for_xml_id("sale_crm.crm_quotation_partner_action")
    #     else:
    #         return self.action_new_quotation()
    # def action_new_quotation(self):
        action = self.env["ir.actions.actions"]._for_xml_id("real-estate-net4x.real_estate_action_quotations_new")
        action['context'] = self._prepare_opportunity_quotation_context()
    #     action['context']['search_default_opportunity_id'] = self.id
        return action

    def _prepare_opportunity_quotation_context(self):
        """ Prepares the context for a new quotation (sale.order) by sharing the values of common fields """
        self.ensure_one()
        product_variant = self.env['product.product'].search([('product_tmpl_id', '=', self.property_id.property_product.id)], limit=1)
        quotation_context = {
            'default_opportunity_id': self.id,
            'default_is_real_estate_lead': True,
            # 'default_partner_id': self.partner_id.id,
            # 'default_campaign_id': self.campaign_id.id,
            # 'default_medium_id': self.medium_id.id,
            # 'default_origin': self.name,
            # 'default_source_id': self.source_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_tag_ids': [(6, 0, self.tag_ids.ids)],
            'default_order_line':[(0, 0, {'product_id': product_variant.id, 'name': self.name, 'product_uom_qty': 1, 'price_unit':self.sales_value})] ,
        }
        # if self.team_id:
        #     quotation_context['default_team_id'] = self.team_id.id
        # if self.user_id:
        #     quotation_context['default_user_id'] = self.user_id.id
        return quotation_context


    def action_view_real_estate_quotation(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations_with_onboarding")
        action['context'] = self._prepare_opportunity_quotation_context()
        action['context']['search_default_draft'] = 1
        action['domain'] = expression.AND([[('opportunity_id', '=', self.id)], self._get_action_view_sale_quotation_domain()])
        quotations = self.order_ids.filtered_domain(self._get_action_view_sale_quotation_domain())
        if len(quotations) == 1:
            action['views'] = [(self.env.ref('real-estate-net4x.real_estate_action_quotations_new').id, 'form')]
            action['res_id'] = quotations.id
        return action




