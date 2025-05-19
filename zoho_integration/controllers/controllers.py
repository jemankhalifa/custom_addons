# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect  # Ensure this import is present
from datetime import datetime  # For datetime class
import requests
import time  # For time.time()
import json
import base64
import logging
_logger = logging.getLogger(__name__)

ZOHO_CLIENT_ID = '1000.5MUZJP26YJIVUU3LYNIIJTSJ2MDO1G'
ZOHO_CLIENT_SECRET = 'a1ac7c094816ceaddab991e6d3be50f3c4cb0b3497'
# REDIRECT_URI = 'http://localhost:8018/zoho/oauth2/callback'
REDIRECT_URI = 'https://7a94-41-45-216-27.ngrok-free.app/zoho/oauth2/callback'

class ZohoIntegration(http.Controller):
    @http.route('/zoho', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/zoho/oauth2/authorize', type='http', auth='user')
    def zoho_start_auth(self, **kwargs):
        auth_url = (
            "https://accounts.zoho.com/oauth/v2/auth"
            "?scope=ZohoBooks.contacts.ALL"
            f"&client_id={ZOHO_CLIENT_ID}"
            "&response_type=code"
            "&access_type=offline"
            f"&redirect_uri={REDIRECT_URI}"
        )
        return redirect(auth_url)  # Using werkzeug's redirect

        # http://localhost:8018/zoho/oauth2/callback?code=1000.7bacd1d61e6f5726ef627bb70cb735b9.a949fcb81bddcab671b9abd06075c2f0&location=us&accounts-server=https%3A%2F%2Faccounts.zoho.com&


    @http.route('/zoho/oauth2/callback', type='http', auth='public', csrf=False)
    def zoho_auth_callback(self, **kwargs):
        code = kwargs.get('code')
        error = kwargs.get('error')

        if error:
            return f"Zoho OAuth Error: {error}"

        if not code:
            return "Missing authorization code."

        # Exchange code for access token
        token_url = "https://accounts.zoho.com/oauth/v2/token"
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': ZOHO_CLIENT_ID,
            'client_secret': ZOHO_CLIENT_SECRET,
        }

        response = requests.post(token_url, data=data)
        if response.status_code != 200:
            return f"Failed to get token: {response.text}"

        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")

        # Step 3: Store the access token and expiry time in ir.config_parameter
        config = request.env['ir.config_parameter'].sudo()
        config.set_param('zoho.access_token', access_token)
        config.set_param('zoho.token_expiry_time', time.time() + expires_in)

        # active_company_id = request.env.user.company_id.id
        # active_company = request.env['res.company'].browse(active_company_id)
        # company = request.env['res.company'].sudo()
        config.set_param('zoho.access_token', access_token)
        config.set_param('zoho.token_expiry_time', time.time() + expires_in)
        active_company = request.env.user.company_id
        active_company.sudo().write({'zoho_access_token': access_token})
        active_company.sudo().write({'zoho_refresh_token': refresh_token})
        active_company.sudo().write({'zoho_expires_in': datetime.fromtimestamp(time.time() + expires_in).strftime('%Y-%m-%d %H:%M:%S')})

        # return access_token

        # ⚠️ Store securely in DB for reuse (this is just a placeholder)
        return f"""
        <h3>Zoho Auth Successful</h3>
        <p><b>Access Token:</b> {access_token}</p>
        <p><b>Refresh Token:</b> {refresh_token}</p>
        <p><b>Expires In:</b> {token_data.get('expires_in')} seconds</p>
        """

    def get_access_token(self):
        # Retrieve stored access token and expiry time
        config = request.env['ir.config_parameter'].sudo()
        access_token = config.get_param('zoho.access_token')
        token_expiry_time = float(config.get_param('zoho.token_expiry_time', default=0))

        # Check if the token has expired
        if time.time() > token_expiry_time:
            # If expired, refresh the token by recalling the authentication flow
            return self.zoho_start_auth()

        return access_token


    @http.route('/zoho/partner/list', type='http', auth='none', csrf=False)
    def make_api_request(self):
        # Retrieve a valid access token (either stored or refreshed)
        access_token = self.get_access_token()

        # Now, use the access token to make a Zoho API request
        # url = "https://books.zoho.com/api/v3/contacts"
        url = "https://www.zohoapis.com/books/v3/contacts"
        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            contacts = response.json().get('contacts', [])
            for contact in contacts:
                # print(f"Contact Name: {contact['contact_name']}")
                _logger.debug(f"************* Contact Name: {contact['contact_name']}")
        else:
            _logger.debug(f"************* Failed to fetch contacts: {response.text}")

    def _update_partner(self,partner, data):
        """Helper function for updates"""
        partner.user_ids[0].write({'name': data.get('contact_name')})
        # partner.write({
        #     # 'name': data.get('contact_name'),
        #     # 'email': data.get('contact_email'),
        #     # Add other fields
        # })

    def _create_partner(self,data):
        """Helper function for creation"""
        partner = request.env['res.partner'].sudo().create({
            'zoho_id': data.get('contact_id'),
            'name': data.get('contact_name'),
            # 'email': data.get('contact_email'),
            # Add other fields
        })
        return partner

    @http.route('/zoho/books', type='http', auth='none', methods=['POST'], csrf=False)
    def update_partner(self, **kwargs):
        try:
            # _logger.info("************* Response received: %s", kwargs)
            zoho_id = kwargs.get('contact_id')
            if not zoho_id:
                return json.dumps({"error": "Missing 'zoho_id'"})
            partner = request.env['res.partner'].sudo()
            contact = partner.search([('zoho_id', '=', zoho_id)], limit=1)
            comment = kwargs.get('zoho_comment', 'Updated/created from Zoho automatic action.')
            if contact:
                self._update_partner(contact, kwargs)
                # contact.message_post(body=comment, author_id=1, message_type='comment', subtype_xmlid='mail.mt_note')
            else:
                self._create_partner(kwargs)
                # contact.message_post(body=comment, author_id=1, message_type='comment', subtype_xmlid='mail.mt_note')
            return json.dumps({"success": True, "partner_id": partner.id})

        except Exception as e:
            _logger.error("Operation failed: %s", str(e))
            return json.dumps({"error": str(e)})
