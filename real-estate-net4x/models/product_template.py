# Part of Odoo. See LICENSE file for full copyright and licensing details.

from math import ceil

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import format_amount


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    property_product = fields.Boolean(
        string="Is Property Product?",
        )
    property_id = fields.Many2one(comodel_name='account.analytic.account',inverse_name='product_id')
    is_property = fields.Boolean(related='property_id.is_property')
    parent_id = fields.Many2one(related='property_id.parent_id')
    property_address = fields.Char(related='property_id.property_address')
    property_type = fields.Many2one(related='property_id.property_type')
    refrence_id = fields.Char(related='property_id.refrence_id')
    floor = fields.Many2one(related='property_id.floor')
    area_size = fields.Float(related='property_id.area_size')
    balcones = fields.Many2one(related='property_id.balcones')
    beds = fields.Many2one(related='property_id.beds')
    # currency_id = fields.Many2one(related='property_id.currency_id')
    # is_published = fields.Boolean(related='property_id.is_published')
    bathroom = fields.Many2one(related='property_id.bathroom')
    furniture = fields.Many2one(related='property_id.furniture')
    parking_spaces = fields.Many2one(related='property_id.parking_spaces')
    maintenance = fields.Many2one(related='property_id.maintenance')
    usage = fields.Many2one(related='property_id.usage')
    view = fields.Char(related='property_id.view')
