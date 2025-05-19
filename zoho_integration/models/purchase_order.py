from odoo import models, fields, api
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import requests




class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    zoho_po_id = fields.Char("Zoho PO ID")
    zoho_sync_date = fields.Datetime("Zoho Sync Date")

    def ensure_vendor_in_zoho(self):
        if self.partner_id.zoho_id:
            return
        else:
            raise UserError(f"Partner {self.partner_id} Not Found in Zoho. Please create it first in zoho")

        token = self.env.user.company_id.zoho_access_token
        org_id = self.env.user.company_id.organization_id
        if not org_id:
            raise UserError("Zoho Organization ID is missing. Please set it in the company settings.")

        data = {
            "contact_name": self.partner_id.name,
            "company_name": self.partner_id.name
        }

        headers = {
            "Authorization": f"Zoho-oauthtoken {token}",
            "Content-Type": "application/json"
        }

        url = f"https://www.zohoapis.com/books/v3/contacts?organization_id={org_id}"
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            self.partner_id.zoho_id = response.json()['contact']['contact_id']
        else:
            raise UserError(f"Failed to create vendor in Zoho: {response.text}")

    def ensure_product_in_zoho(self, product):
        tmpl = product.product_tmpl_id
        if tmpl.zoho_id:
            return
        else:
            raise UserError(f"product {product.name} Not Found in Zoho. Please create it first in zoho")

        token = self.env.user.company_id.zoho_access_token
        org_id = self.env.user.company_id.organization_id
        if not org_id:
            raise UserError("Zoho Organization ID is missing. Please set it in the company settings.")

        data = {
            "name": tmpl.name,
            "rate": tmpl.list_price,
            "purchase_rate": tmpl.standard_price or 0.0,
            "sku": tmpl.default_code or ""
        }

        headers = {
            "Authorization": f"Zoho-oauthtoken {token}",
            "Content-Type": "application/json"
        }

        url = f"https://www.zohoapis.com/books/v3/items?organization_id={org_id}"
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            tmpl.zoho_id = response.json()['item']['item_id']
        else:
            raise UserError(f"Failed to create product '{tmpl.name}' in Zoho: {response.text}")

    def _prepare_zoho_payload(self):
        self.ensure_one()
        line_items = []
        for line in self.order_line:
            self.ensure_product_in_zoho(line.product_id)
            line_items.append({
                "item_id": line.product_id.product_tmpl_id.zoho_id,
                "rate": line.price_unit,
                "quantity": line.product_qty,
                "name": line.name,
            })

        return {
            "vendor_id": self.partner_id.zoho_id,
            "reference_number": self.name,
            "date": self.date_order.strftime('%Y-%m-%d'),
            "line_items": line_items,
        }

    def export_po_to_zoho(self):
        for po in self:
            if po.zoho_po_id:
                continue

            po.ensure_vendor_in_zoho()
            payload = po._prepare_zoho_payload()

            token = self.env.user.company_id.zoho_access_token
            org_id = self.env.user.company_id.organization_id

            headers = {
                "Authorization": f"Zoho-oauthtoken {token}",
                "Content-Type": "application/json"
            }

            url = f"https://www.zohoapis.com/books/v3/purchaseorders?organization_id={org_id}"
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 201:
                result = response.json()
                po.write({
                    "zoho_po_id": result['purchaseorder']['purchaseorder_id'],
                    "zoho_sync_date": fields.Datetime.now(),
                })
            else:
                raise UserError(f"Zoho Error: {response.text}")
