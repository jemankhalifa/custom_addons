from odoo import api, fields, models, _
from odoo.exceptions import UserError
from lxml import etree
from lxml.etree import XML, tostring
from .xml_template import *


class wkf_node(models.Model):
    _name = "wkf.node"
    _description = "Wkf Node"
    _order = 'sequence'

    name = fields.Char(string='Name', required=True, help='A node is basic unit of Workflow')
    sequence = fields.Integer(string='Sequence')
    code = fields.Char(string='Code', required=False)
    wkf_id = fields.Many2one('wkf.base', string='Workflow', required=True, index=True, ondelete='cascade')
    split_mode = fields.Selection([('OR', 'Or'),
                                   ('AND', 'And')], string='Split Mode', size=3, required=False)
    join_mode = fields.Selection([('OR', 'Or'),
                                  ('AND', 'And')],
                                 string='Join Mode', size=3, required=True, default='OR',
                                 help='OR:anyone input Transfers approved, will arrived this node.  AND:must all input Transfers approved, will arrived this node')
    action = fields.Char(string='Python Action', size=64,
                         help='When arrived this node, you can set to trigger a object function to do something, example confirm the order')
    arg = fields.Text(string='Action Args', size=64, help='the object function args')
    is_start = fields.Boolean(string='Workflow Start', help='This node is the start of the Workflow')
    is_stop = fields.Boolean(string='Workflow Stop', help='This node is the end of the Workflow')
    out_trans = fields.One2many('wkf.trans', 'node_from', string='Out Transfer', help='The out transfer of this node')
    in_trans = fields.One2many('wkf.trans', 'node_to', string='Incoming Transfer',
                               help='The input transfer of this node')
    show_state = fields.Boolean(string='Show In Workflow', default=True,
                                help="If True, This node will show in Workflow states")
    no_reset = fields.Boolean(string='Invisible Reset', default=True,
                              help="If True, this Node not display the Reset button, default is True")
    event_need = fields.Boolean(string='Create event',
                                help="If true, When Workflow arrived this node, will create a calendar event relation users")
    event_users = fields.Many2many('res.users', 'event_users_trans_ref', 'tid', 'uid', string='Event Users',
                                   help="The calendar event users")

    def backward_cancel_logs(self, res_id):
        """
        cancel the logs from this node, and create_date after the logs
        """
        log_obj = self.env['wkf.log.trans']
        logs = log_obj.search([('res_id', '=', res_id), ('trans_id.node_from.id', '=', self.id)])
        if logs:
            min_date = min([x.create_date for x in logs])
            logs2 = log_obj.search([('res_id', '=', res_id), ('create_date', '>=', min_date)])
            logs.write({'active': False})
            logs2.write({'active': False})

    def check_trans_in(self, res_id):
        self.ensure_one()

        flag = True
        join_mode = self.join_mode
        log_obj = self.env['wkf.log.trans']

        flag = False
        if join_mode == 'OR':
            flag = True
        else:
            in_trans = filter(lambda x: x.is_backward is False, self.in_trans)
            trans_ids = [x.id for x in in_trans]
            logs = log_obj.search([('res_id', '=', res_id), ('trans_id', 'in', trans_ids)])
            log_trans_ids = [x.trans_id.id for x in logs]
            flag = set(trans_ids) == set(log_trans_ids) and True or False

        return flag

    def make_event(self, name):
        data = {
            'name': '%s %s' % (name, self.name),
            'partner_ids': [(6, 0, [u.partner_id.id for u in self.event_users])],
            'start': fields.Datetime.now(),
            'stop': fields.Datetime.now(),
            'duration': 1,
        }
        self.env['calendar.event'].create(data)
        return True
