from odoo import models, fields, api

class PropertyTypes(models.Model):
    _name = 'property.types'
    _description = "Property Types"

    name = fields.Char(string="Property Type")


class PropertyFloor(models.Model):
    _name = 'property.floor'
    _description = "Property Floor"

    name = fields.Char(string="Floor")


class PropertyBalcones(models.Model):
    _name = 'property.balcones'
    _description = "Property Balcones"

    name = fields.Char(string="Balcones")

class PropertyBeds(models.Model):
    _name = 'property.beds'
    _description = "Property Beds"

    name = fields.Char(string="Beds")

class PropertyBaths(models.Model):
    _name = 'property.baths'
    _description = "Property Baths"

    name = fields.Char(string="Baths")

class PropertyFurnitureType(models.Model):
    _name = 'property.furniture.type'
    _description = "Property furniture Type"

    name = fields.Char(string="Type")
class PropertyUsage(models.Model):
    _name = 'property.usage'
    _description = "Property Usage"

    name = fields.Char(string="Usage")

class PropertyParking(models.Model):
    _name = 'property.parking.spaces'
    _description = "Property parking spaces"

    name = fields.Char(string="Parkings")

class PropertyMaintenance(models.Model):
    _name = 'maintenance.services.types'
    _description = "Property Maintenance Services Types"

    name = fields.Char(string="Type")

class PropertyStage(models.Model):
    _name = 'property.stage'
    _description = "Property Stage"

    name = fields.Char(string="Stage")
    sequence = fields.Char(string="Sequence")
