from odoo import models, fields, api

class AnalyticAccoounts(models.Model):
    _inherit = 'account.analytic.account'

    for_sale = fields.Boolean(string="For Sale?")
    for_rent = fields.Boolean(string="For Rent?")
    refrence_id = fields.Char(string="Refrence?")
    property_type = fields.Many2one('property.types',string="Property Type")
    floor = fields.Many2one('property.floor',string="Floor")
    area_size = fields.Float(string="Area Size sqft")
    balcones = fields.Many2one('property.balcones',string="Balcones")
    beds = fields.Many2one('property.beds',string="Beds")
    bathroom = fields.Many2one('property.baths',string="Bathroom")
    furniture = fields.Many2one('property.furniture.type',string="Furnitued?")
    parking_spaces = fields.Many2one('parking.spaces',string="Parking Spaces")
    maintenance = fields.Many2one('maintenance.services.types',string="Maintenance")
    usage = fields.Many2one('property.usage',string="Usage")
    view = fields.Char(string="View")


