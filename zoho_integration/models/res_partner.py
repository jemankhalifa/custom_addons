from odoo import models,fields,api,modules
from odoo.exceptions import UserError
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):

        _logger.info(f'########### {vals}')

        return super().create(vals)

    zoho_id = fields.Char("Zoho ID")
    # is_zoho = fields.Boolean("Zoho ?")

    def is_valid_string(self,value):
        """Check if a string is not empty or invalid."""
        return isinstance(value, str) and value.strip() != ""

    def validate_dict(self,data):
        """Construct dict with only valid fields."""
        # Assuming data is a list of dictionaries
        valid_data = []
        
        for item in data:
            if isinstance(item, dict):  # Ensure each item is a dictionary
                # Create a new dictionary with only valid fields
                valid_item = {key: value for key, value in item.items() if self.is_valid_string(value)}
                valid_data.append(valid_item)
        return valid_data

    def zoho_contact_dict(self, contact, type='create'):
        # bank_info=self.env['res.partner.bank'].search([('partner_id','=',contact.id)],limit=1)
        contact_info = [{
            'contact_name':contact.name,
            'company_name':contact.company_id.name,
            # 'contact_type':contact.type,
            # 'phoneNumber':contact.phone, 
            # 'email':contact.email, 
            # 'accountNumber':bank_info.acc_number
        }]
        if type == 'update':
            contact_info[0] = {'contact_id': contact.zoho_id, **contact_info[0]}
        contact_data = self.validate_dict(contact_info)
        return contact_data

    def get_zoho_token(self):
        expires_in = self.company_id.zoho_expires_in
        now = fields.Datetime.now()
        if not expires_in or fields.Datetime.from_string(expires_in) <= fields.Datetime.from_string(now):
            # Token has expired or not set, regenerate here
            self.company_id.zoho_auth()
        return self.company_id.zoho_access_token

    def zoho_request(self, method, endpoint, data=None, params=None):
        # bundle_alias = self.env['ir.config_parameter'].sudo().get_param('freshsales_bundle_alias')
        # access_token = self.env['ir.config_parameter'].sudo().get_param('zoho.access_token')
        access_token = self.get_zoho_token()
        # url = bundle_alias + '/api/' + endpoint
        url = "https://www.zohoapis.com/books/v3/" + endpoint
        data_json_str = json.dumps(data[0])
        # data_json_str = json_data[1:-1]  # Remove first and last characters
        headers = {
          'Authorization': f"Zoho-oauthtoken {access_token}",
        }
          # 'Content-Type': 'application/json',
          #   'User-Agent': 'Chrome v22.2 Linux Ubuntu',
          #   'Accept': '*/*',
          #   'Accept-Encoding': 'gzip, deflate, br',
          #   'Connection': 'keep-alive',
          #   'X-Requested-With': 'XMLHttpRequest'
        response = requests.request(method, url, headers=headers,params=params, data=data_json_str)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise UserError(f'Error: {response.status_code}, {response.text}')

    def git_zoho_contacts(self, account=None):
        if not account:
            account=self
        endpoint = 'contacts'
        # list_contacts = self.zoho_request('GET', endpoint, account_data)
        list_contacts = self.zoho_request('GET', endpoint)


    def create_zoho_contact(self, contact=None):
        if not contact:
            contact=self
        contact_data = self.zoho_contact_dict(contact)
        created_contact = self.zoho_request('POST', 'contacts', data=contact_data)
        contact.write({
            # 'zoho_id':created_contact.get('contact_id')
            'zoho_id':created_contact['contact']['contact_id']
            })
        self.env.cr.commit()
