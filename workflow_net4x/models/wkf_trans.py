from odoo import api, fields, models, _
from odoo.exceptions import UserError
from lxml import etree
from lxml.etree import XML, tostring
from .xml_template import *


class wkf_trans(models.Model):
    _name = "wkf.trans"
    _description = "Wkf Trans"
    _order = "sequence"

    @api.depends('group_ids')
    def _compute_xml_groups(self):
        data_obj = self.env['ir.model.data']
        xml_ids = []
        for g in self.group_ids:
            data = data_obj.search([('res_id', '=', g.id), ('model', '=', 'res.groups')])
            xml_ids.append(data.complete_name)
        self.xml_groups = xml_ids and ','.join(xml_ids) or False

    name = fields.Char(string='Name', required=True, help='A transfer is from a node to other node')
    code = fields.Char(string='Code', required=False)
    group_ids = fields.Many2many('res.groups', 'group_trans_ref', 'tid', 'gid', string='Groups',
                                 help="The groups who can process this transfer")
    user_ids = fields.Many2many('res.users', 'user_trans_ref', 'tid', 'uid', string='Users',
                                help="The Users who can process this transfer")
    condition = fields.Char(string='Condition', required=True, default='True',
                            help='The check condition of this transfer, default is True')
    node_from = fields.Many2one('wkf.node', string='From Node', required=True, index=True, ondelete='cascade', )
    node_to = fields.Many2one('wkf.node', string='TO Node', required=True, index=True, ondelete='cascade')
    wkf_id = fields.Many2one('wkf.base', related='node_from.wkf_id', store=True)
    model = fields.Char(related='wkf_id.model')
    xml_groups = fields.Char(compute='_compute_xml_groups', string='XML Groups')
    is_backward = fields.Boolean(string='Is Reverse', help="Is a Reverse transfer")
    auto = fields.Boolean(string='Auto',
                          help="If true, when condition is True,transfer will auto finish, not need button, default false")
    sequence = fields.Integer(string='Sequence')
    need_note = fields.Boolean(string='Force note',
                               help="If true, the Workflow note can not be empty, usually when transfer is Reverse,you need it")

    def make_log(self, res_name, res_id, note=''):
        return self.env['wkf.log.trans'].create({'name': res_name, 'res_id': res_id, 'trans_id': self.id, 'note': note})
