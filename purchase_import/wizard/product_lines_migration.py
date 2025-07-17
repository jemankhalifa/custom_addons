from odoo import _, api, fields, models
from datetime import date


class OrderLinesMigration(models.Model):
    _name = 'order.lines.migration'

    order_date = fields.Date('Order date', required=True)
    supplier_id = fields.Many2one('res.partner', string="Supplier", required=True)
    order_type = fields.Selection([
        ('requisition', 'Requisition'),
        ('done_order', 'Done Order')
    ], string="Order type")

    def create_migration_order(self):
        OrderLineData = self.env['purchase.order.line.data']
        PurchaseOrder = self.env['purchase.order']
        lines = []

        if self._context.get('active_ids'):
            records = OrderLineData.browse(self._context['active_ids'])

            for rec in records:
                vals = rec._prepare_compute_all_values()
                taxes = rec.taxes_id.compute_all(
                    price_unit=vals['price_unit'],
                    currency=vals['currency_id'],
                    quantity=vals['product_qty'],
                    product=vals['product'],
                    partner=vals['partner']
                )

                subtotal = taxes['total_included'] - (taxes['total_excluded'] * (rec.discount / 100))
                line_vals = {
                    'product_id': rec.product_id.id,
                    'product_qty': rec.product_qty,
                    'price_unit': rec.price_unit,
                    'discount': rec.discount,
                    'name': rec.name,
                    'date_planned': rec.date_planned,
                    'product_uom': rec.product_uom.id,
                    'price_subtotal': subtotal,
                    'price_total': subtotal,
                    'taxes_id': [(6, 0, rec.taxes_id.ids)],
                }
                lines.append((0, 0, line_vals))

            order = PurchaseOrder.create({
                'date_order': self.order_date,
                'partner_id': self.supplier_id.id,
                'order_line': lines,
            })

            if self.order_type == 'done_order':
                order.button_confirm()

            return {
                'name': f"{self.order_date} {self.supplier_id.name}",
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.order',
                'res_id': order.id,
                'view_mode': 'form',
                'target': 'current',
            }
