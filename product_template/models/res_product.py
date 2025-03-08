from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    restrict_based_on_capacity = fields.Boolean(string="Restrict Based on Current Capacity", config_parameter="sale_subscription.restrict_based_on_capacity")

    def create(self, vals):
        product_id = vals.get('product_id')
        restrict_based_on_capacity = self.env['ir.config_parameter'].sudo().get_param('sale_subscription.restrict_based_on_capacity')
        
        if product_id and restrict_based_on_capacity:
            product = self.env['product.product'].browse(product_id)
            if product.product_tmpl_id.current_capacity <= 0:
                raise models.ValidationError(_("Sorry, there is no capacity now for this service."))
        return super(SaleSubscription, self).create(vals)