from odoo import models, fields, api
from odoo.exceptions import ValidationError 
import logging

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    capacity = fields.Integer(string="Capacity", required=True, default=1)
    current_capacity = fields.Integer(string="Current Capacity", compute="_compute_current_capacity", store=True)
    quotation_ids = fields.One2many('sale.order', 'quotation_template_id', string="Quotations")
    _logger = logging.getLogger(__name__)
    _logger.info("🚀 هذا هو نص التجربة!")  # سيظهر في السجلات
    print("****Computing Current Capacity...****")
    @api.depends('capacity', 'quotation_ids.state')
    def _compute_current_capacity(self):
        "حساب السعة الحالية بناءً على عدد عروض الأسعار المؤكدة."
        print("****Computing Current Capacity...****")
        _logger = logging.getLogger(__name__)

        _logger.info("🚀 هذا هو نص التجربة!")  # سيظهر في السجلات
        _logger.debug("🛠 رسالة تصحيحية لمزيد من التفاصيل")
        for record in self:
            active_quotations = record.quotation_ids.filtered(lambda q: q.state == 'sale')
            record.current_capacity = max(0, record.capacity - len(active_quotations))
            print(f"***** {record.name}: Capacity Updated to {record.current_capacity}**********")

    def decrease_capacity(self):
        "إنقاص السعة عند تأكيد الطلب."
        print(f"******Decreasing Capacity for {self.name}*******")
        self.ensure_one()
        if self.current_capacity > 0:
            self.current_capacity -= 1
