from odoo import models, fields, api

class AnalyticAccounts(models.Model):
    _inherit = 'account.analytic.account'

    for_sale = fields.Boolean(string="For Sale?")
    for_rent = fields.Boolean(string="For Rent?")
    is_real_estate = fields.Boolean(string="Is real estate nalytic account", default=False)
    is_property = fields.Boolean(string="Is Property?", default=False)
    parent_id = fields.Many2one('account.analytic.account', string="Parent" , domain=[('is_real_estate', '=', True)])
    stage_id = fields.Many2one('property.stage', string="Stage" , ondelete='cascade')
    real_estate_image = fields.Image(string='Property Image')
    contract_id = fields.Many2one('sale.order', string="Contract")
    refrence_id = fields.Char(string="Refrence?")
    property_type = fields.Many2one('property.types',string="Property Type")
    property_address = fields.Char('Address', readonly=False, store=True)
    is_published = fields.Boolean(string="Published")
    floor = fields.Many2one('property.floor',string="Floor")
    area_size = fields.Float(string="Area Size sqft")
    balcones = fields.Many2one('property.balcones',string="Balcones")
    beds = fields.Many2one('property.beds',string="Beds")
    bathroom = fields.Many2one('property.baths',string="Bathroom")
    furniture = fields.Many2one('property.furniture.type',string="Furnitued?")
    parking_spaces = fields.Many2one('property.parking.spaces',string="Parking Spaces")
    maintenance = fields.Many2one('maintenance.services.types',string="Maintenance")
    usage = fields.Many2one('property.usage',string="Usage")
    view = fields.Char(string="View")
    website_description = fields.Text(string="Description")
    attachment_image_ids = fields.Many2many('ir.attachment','real_estate_property_attachment_image_rel')
    attachment_doc_ids = fields.Many2many('ir.attachment','real_estate_property_attachment_doc_rel')
    product_id = fields.One2many(comodel_name='product.template',inverse_name='property_id' )
    property_product = fields.Many2one(comodel_name='product.template')
    property_product_created = fields.Boolean(default=False)
    @api.model
    def create(self, vals):
        # Modify vals to include default values or context
        if 'plan_id' not in vals:
            # Set a default value for plan_id if not provided
            vals['plan_id'] = self.env.ref('real-estate-net4x.real_estate_analytic_plan_properties').id
            vals['stage_id'] = self.env.ref('real-estate-net4x.reale_state_stage_draft').id
        record = super(AnalyticAccounts, self).create(vals)
        return record

    def action_confirme(self):
        for rec in self:
            rec.action_create_product()
            rec.stage_id = self.env.ref('real-estate-net4x.reale_state_stage_confirmed').id
    def action_create_product(self):
        self.ensure_one()
        property_product = self.env['product.template'].create({
            "name": self.name,
            "property_product": True,
            "property_id": self.id,
            # "parent_id": self.parent_id,
            # "property_address": self.property_address,
            # "property_type": self.property_type,
            # "refrence_id": self.refrence_id,
            # "floor": self.floor,
            # "balcones": self.balcones,
            # "beds": self.beds,
            # # "currency_id": self.currency_id,
            # "is_published": self.is_published,
            # "bathroom": self.bathroom,
            # "furniture": self.furniture,
            # "parking_spaces": self.parking_spaces,
            # "maintenance": self.maintenance,
            # "usage": self.usage,
            # "view": self.view,
   

            "image_1920": self.real_estate_image,


            "type": 'service',
            "default_code": "RENTAL",
            "purchase_ok": False,
        })
        self.property_product = property_product
        self.property_product_created = True

    def action_create_lead(self):
        self.ensure_one()
        lead = self.env['crm.lead'].create({
            'property_id': self.id,
            'name': self.name,
            'is_real_estate_lead' : True,
            # 'partner_id': self.contact_company.id,
        })
        