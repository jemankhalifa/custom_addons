from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quotation_template_id = fields.Many2one('sale.order.template', string="Quotation Template")

    @api.onchange('quotation_template_id')
    def _onchange_quotation_template(self):
        """تحذير إذا لم يكن هناك سعة متاحة عند اختيار قالب عرض السعر."""
        if self.quotation_template_id and self.quotation_template_id.current_capacity == 0:
            print("****** Capacity Full Warning Triggered *****")
            return {
                'warning': {
                    'title': "Capacity Full!",
                    'message': "Sorry, there is no capacity available for this service.",
                }
            }

    def action_confirm(self):
        """تحديث سعة النموذج عند تأكيد الطلب."""
        print(f"**** Confirming Order: {self.name}*******")
        for order in self:
            if order.quotation_template_id:
                template = order.quotation_template_id
                print(f"****** Current Capacity (Before): {template.current_capacity}*****")
                if template.current_capacity <= 0:
                    raise ValidationError("Sorry, there is no capacity available for this service.")

                # إنقاص السعة يدوياً
                template.decrease_capacity()
                print(f"********** Current Capacity (After): {template.current_capacity}*****")
    
        return super(SaleOrder, self).action_confirm()
