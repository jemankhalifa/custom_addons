from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
from datetime import datetime
import requests
import time
import json
import base64
import logging
_logger = logging.getLogger(__name__)


class ZohoWebhookController(http.Controller):

    @http.route('/zoho/webhook/purchase_order', type='http', auth='public', csrf=False)
    def receive_po(self, **kwargs):
        _logger.info('*****************************')
        _logger.info(kwargs)
        _logger.info('****************')


        # payload = request.jsonrequest
        # _logger.info(f"[ZOHO PO Webhook] Payload: {payload}")
        #
        # zoho_po_id = payload.get('purchaseorder_id')
        # if not zoho_po_id:
        #     return {"error": "Missing purchaseorder_id"}
        #
        # po_model = request.env['purchase.order'].sudo()
        # existing = po_model.search([('zoho_po_id', '=', zoho_po_id)], limit=1)
        #
        # partner = request.env['res.partner'].sudo().search([('zoho_id', '=', payload['vendor_id'])], limit=1)
        # if not partner:
        #     return {"error": "Vendor not found"}
        #
        # lines = []
        # for item in payload.get('line_items', []):
        #     product = request.env['product.product'].sudo().search([('product_tmpl_id.zoho_id', '=', item['item_id'])],
        #                                                            limit=1)
        #     if product:
        #         lines.append((0, 0, {
        #             'product_id': product.id,
        #             'name': item['name'],
        #             'product_qty': item['quantity'],
        #             'price_unit': item['rate']
        #         }))
        #
        # if existing:
        #     existing.write({'order_line': [(5, 0, 0)] + lines})
        # else:
        #     po_model.create({
        #         'partner_id': partner.id,
        #         'zoho_po_id': zoho_po_id,
        #         'date_order': payload.get('date'),
        #         'order_line': lines
        #     })
        #
        # return {"status": "success"}
