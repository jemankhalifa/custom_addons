from odoo import api, fields, models, _
from odoo.exceptions import UserError
from lxml import etree
from lxml.etree import XML, tostring
from .xml_template import *


class wkf_log_trans(models.Model):
    _name = "wkf.log.trans"
    _description = "Wkf log"

    name = fields.Char(string='Name')
    trans_id = fields.Many2one('wkf.trans', string='Transfer')
    model = fields.Char(related='trans_id.model', string='Model')
    res_id = fields.Integer(string='Resource ID')
    active = fields.Boolean(string='Active', default=True)
    note = fields.Text(string='Note', help="If you want record something for this transfer, write here")
