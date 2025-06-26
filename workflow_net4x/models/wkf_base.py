from odoo import api, fields, models, _
from odoo.exceptions import UserError
from lxml import etree
from lxml.etree import XML, tostring
from .xml_template import *


class wkf_base(models.Model):
    _name = 'wkf.base'
    _description = 'Wkf Base'
    _def_wkf_state_name = 'x_wkf_state'
    _def_wkf_note_name = 'x_wkf_note'

    @api.depends('node_ids')
    def _compute_default_state(self):
        def _get_start_state(nodes):
            if not nodes: return None
            star_id = nodes[0].id
            for n in nodes:
                if n.is_start:
                    star_id = n.id
                    break
            return str(star_id)

        nodes = self.node_ids
        show_nodes = filter(lambda x: x.show_state, nodes)
        no_rest_nodes = filter(lambda x: x.no_reset, nodes)

        self.show_states = ','.join([str(x.id) for x in show_nodes])
        self.default_state = _get_start_state(nodes)
        self.no_reset_states = ','.join(["'%s'" % x.id for x in no_rest_nodes])

    @api.model
    def _default_reset_group(self):
        return self.env.ref('base.group_system').id

    name = fields.Char(srting='Name', required=True, )
    model_id = fields.Many2one('ir.model', srting='Module ID', required=True, ondelete='cascade',
                               help="Select a model that you want to create the Workflow")
    model = fields.Char(related='model_id.model', string='Model Name', readonly=True)
    model_view_id = fields.Many2one('ir.ui.view', srting='Model  View',
                                    help='The form view of the model that want to extend Workflow button on it')
    view_id = fields.Many2one('ir.ui.view', srting='Add View', readonly=True,
                              help='The auto created Workflow extend view, show Workflow button, state, logs..', )
    node_ids = fields.One2many('wkf.node', 'wkf_id', srting='Node', help='Nodes')
    trans_ids = fields.One2many('wkf.trans', 'wkf_id', srting='Transfer', help='Transfers,')
    active = fields.Boolean(srting='Active', default=True)
    field_id = fields.Many2one('ir.model.fields', srting='Field Workflow-State', help='The Workflow State field',
                               readonly=True)
    tracking = fields.Integer(srting='Tracking Wkf state', default=1)

    allow_reset = fields.Boolean(srting='Allow to reset the Workflow', default=True,
                                 help='If True, This Workflow allow to reset draft')
    reset_group = fields.Many2one('res.groups', srting='Group Reset', default=_default_reset_group, required=True,
                                  help='Workflow Reset Button Groups, default Admin')
    no_reset_states = fields.Char(compute='_compute_default_state', string='No Reset States',
                                  help='Which state u can to reset the Workflow')

    default_state = fields.Char(compute='_compute_default_state', string='Default Workflow State value', store=False,
                                help='The default Workflow state, It is come from the star node')
    show_states = fields.Char(compute='_compute_default_state', string='Default  States to display', store=False,
                              help='Which status can show the state widget, It is set by node')

    @api.constrains('model_id')
    def check_uniq(self):
        for one in self:
            if self.search_count([('model_id', '=', one.model_id.id)]) > 1:
                raise UserError('workflow must be unique fer model')

    @api.model
    def get_default_state(self, model):
        return self.search([('model', '=', model)]).default_state

    def sync2ref_model(self):
        self.ensure_one()
        self._check()
        self.make_field()
        self.make_view()

    def _check(self):
        if not any([n.is_start for n in self.node_ids]):
            raise UserError('Please check the nodes setting, not found a start node')

    def make_wkf_contain(self):
        wkf_contain = XML(wkf_contain_template)
        wkf_contain.append(self.make_btm_contain())
        wkf_contain.append(XML(wfk_field_state_template % (self.field_id.name, self.show_states)))
        return wkf_contain

    def make_btm_contain(self):
        btn_contain = XML(bton_contain_template)
        for t in self.trans_ids:
            btn = XML(btn_template % {'btn_str': t.name,
                                      'trans_id': t.id,
                                      'vis_state': t.node_from.id})
            if t.group_ids:
                btn.set('groups', t.xml_groups)
            if t.user_ids:
                user_ids_str = ','.join([str(x.id) for x in t.user_ids])
                btn.set('user_ids', user_ids_str)
            btn_contain.append(btn)

        btn_contain.append(XML(btn_show_log_template % {'btn_str': 'Show Trans Logs', 'btn_grp': 'base.group_user'}))
        btn_contain.append(XML(btn_wkf_reset_template % {'btn_str': 'Reset Workflow', 'btn_grp': 'base.group_system',
                                                         'btn_ctx': self.id,
                                                         'no_reset_states': self.no_reset_states}))
        return btn_contain

    def make_view(self):
        self.ensure_one()
        view_obj = self.env['ir.ui.view']
        have_header = '<header>' in self.model_view_id.arch
        arch = have_header and XML(arch_template_header) or XML(arch_template_no_header)

        wkf_contain = self.make_wkf_contain()

        arch.insert(0, wkf_contain)

        view_data = {
            'name': '%s.WKF.form.view' % self.model,
            'type': 'form',
            'model': self.model,
            'inherit_id': self.model_view_id.id,
            'mode': 'extension',
            'arch': tostring(arch),
            'priority': 99999,
        }

        # update or create view
        view = self.view_id
        if not view:
            view = view_obj.create(view_data)
            self.write({'view_id': view.id})
        else:
            view.write(view_data)

        return True

    def make_field(self):
        self.ensure_one()
        fd_obj = self.env['ir.model.fields']
        fd_id = fd_obj.search([('name', '=', self._def_wkf_state_name), ('model_id', '=', self.model_id.id)])
        fd_id2 = fd_obj.search([('name', '=', self._def_wkf_note_name), ('model_id', '=', self.model_id.id)])
        fd_data = {
            'name': self._def_wkf_state_name,
            'ttype': 'selection',
            'state': 'manual',
            'model_id': self.model_id.id,
            'model': self.model_id.model,
            'modules': self.model_id.modules,
            'tracking': self.tracking,
            'field_description': u'WorkFollow State',
            'selection': str(self.get_state_selection()),
        }
        if fd_id:
            fd_id.write(fd_data)
        else:
            fd_id = fd_obj.create(fd_data)

        self.write({'field_id': fd_id.id})
        return True

    @api.model
    def get_state_selection(self):
        return [(str(i.id), i.name) for i in self.node_ids]

    def action_no_active(self):
        self.ensure_one()
        self.view_id.unlink()
        self.field_id.unlink()
        return True
