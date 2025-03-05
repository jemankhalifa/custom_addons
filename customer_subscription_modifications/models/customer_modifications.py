from odoo import models, fields, api
import random
import string

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_id = fields.Char(string="Customer ID")

    def print_subscriber_card(self):
        return self.env.ref('customer_id.action_subscriber_card_report').report_action(self)



   

