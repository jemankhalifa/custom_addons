from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'sale.order'

    capacity = fields.Integer(string="Capacity", default=0)
    current_capacity = fields.Integer(string="Current Capacity", compute="_compute_current_capacity", store=True)

    @api.depends('capacity')
    def _compute_current_capacity(self):
        Subscription = self.env.get('sale.subscription')  # تحقق من وجود النموذج
        if Subscription:
            for product in self:
                active_subscriptions = Subscription.search_count([
                    ('product_id', '=', product.id),
                    ('stage_id.is_in_progress', '=', True)
                ])
                product.current_capacity = product.capacity - active_subscriptions
        else:
            # إذا لم تكن الوحدة مثبتة
            for product in self:
                product.current_capacity = product.capacity
