from odoo import models, fields, api

class PropertyTypes(models.Model):
    _name = 'property.types'

    name = fields.Char(string="Property Type")


class PropertyFloor(models.Model):
    _name = 'property.floor'

    name = fields.Char(string="Floor")


class PropertyBalcones(models.Model):
    _name = 'property.balcones'

    name = fields.Char(string="Balcones")

class PropertyBeds(models.Model):
    _name = 'property.beds'

    name = fields.Char(string="Beds")

class PropertyBaths(models.Model):
    _name = 'property.baths'

    name = fields.Char(string="Baths")

class PropertyFurnitureType(models.Model):
    _name = 'property.furniture.type'

    name = fields.Char(string="Type")

class PropertyParking(models.Model):
    _name = 'parking.spaces'

    name = fields.Char(string="Parkings")

class PropertyMaintenance(models.Model):
    _name = 'maintenance.services.types'

    name = fields.Char(string="Type")

class PropertyUsage(models.Model):
    _name = 'property.usage'

    name = fields.Char(string="Usage")