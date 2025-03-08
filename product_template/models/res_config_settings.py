from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    restrict_based_on_capacity = fields.Boolean(string="Restrict Based on Current Capacity", config_parameter="sale_subscription.restrict_based_on_capacity")

