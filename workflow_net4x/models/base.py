from lxml import etree
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.addons.base.models.ir_ui_view import Model as BM
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)


def wkf_trans_condition_expr_eval(self, lines):
    result = False

    for line in lines.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line == 'True':
            result = True
        elif line == 'False':
            result = False
        else:
            result = eval(line)
    return result


# Set default state
default_get_old = BM.default_get


@api.model
def default_get_new(self, fields_list):
    res = default_get_old(self, fields_list)
    if 'x_wkf_state' in fields_list:
        res.update({'x_wkf_state': self.env['wkf.base'].get_default_state(self._name)})
    return res


def wkf_button_action(self):
    ctx = self.env.context.copy()
    _logger.info('wkf_button_action %s' % self.env.context)
    t_id = int(self.env.context.get('trans_id'))
    trans = self.env['wkf.trans'].browse(t_id)

    if trans.need_note:
        return {
            'name': _('Workflow Approval'),
            'view_type': 'form',
            "view_mode": 'form',
            'res_model': 'wizard.wkf.message',
            'type': 'ir.actions.act_window',
            # 'view_id': False,
            'target': 'new',
            'context': ctx,
        }
    else:
        return self.wkf_action()


def wkf_action(self, message=''):
    t_id = int(self.env.context.get('trans_id'))
    trans = self.env['wkf.trans'].browse(t_id)

    # condition_ok = eval(trans.condition)
    condition_ok = wkf_trans_condition_expr_eval(self, trans.condition)
    _logger.info('>>>>>>%s: %s', trans.condition, condition_ok)

    if not condition_ok:
        if trans.auto:
            _logger.info('condition false:%s', trans.condition)
            return True
        else:
            raise UserError(u'Th condition is not allow to trans, Pleas contract with Administrator')

    # check repeat trans
    if not trans.is_backward:
        if self.env['wkf.log.trans'].search([('res_id', '=', self.id), ('trans_id', '=', t_id)], limit=1):
            raise UserError(_('The transfer had finish'))

    # check note
    if trans.need_note and not self.x_wkf_note:
       raise UserError(_('The transfer can not empty note'))

    log = trans.make_log(self._name, self.id, message)

    # check  can be trans
    node_to = trans.node_to
    node_from = trans.node_from
    can_trans = node_to.check_trans_in(self.id)
    if can_trans:
        self.write({'x_wkf_state': str(node_to.id)})
        action, arg = node_to.action, node_to.arg
        # action
        if trans.is_backward:
            node_to.backward_cancel_logs(self.id)
        else:
            if action:
                _logger.info('======action:%s, arg:%s', action, arg)
                if arg:
                    getattr(self, action)(eval(arg))
                else:
                    getattr(self, action)()

        # 2:calendar event
        if node_to.event_need:
            node_to.make_event(self.name)

        # # message to user
        # self.message_post(
        #     body='%s %s' % (self.name, node_to.name),
        #     message_type="comment",
        #     subtype="mail.mt_comment",
        #     partner_ids=[u.partner_id.id for u in node_to.event_users],
        # )

        # 3 auto trans
        auto_trains = filter(lambda t: t.auto, node_to.out_trans)
        for auto_t in auto_trains:
            self.with_context(trans_id=auto_t.id).wkf_button_action()

    return True


def wkf_button_show_log(self):
    return {
        'name': _('WorkFollow Logs'),
        'view_mode': 'list,form',
        'view_type': 'form',
        'res_model': 'wkf.log.trans',
        'type': 'ir.actions.act_window',
        'target': 'new',
        'domain': [('res_id', '=', self[0].id,)],
    }


def wkf_button_reset(self):
    logs = self.env['wkf.log.trans'].search([('res_id', '=', self[0].id), ('model', '=', self._name)])
    logs.write({'active': False})
    wkf_id = self.env.context.get('wkf_id')
    state = self.env['wkf.base'].browse(wkf_id).default_state
    self.write({'x_wkf_state': state})
    return True

    # default_x_state =


old_get_view = BM.get_view


@api.model
def new_get_view(self, view_id=None, view_type='form', **options):
    """<button   user_ids="1,2,3" """
    res = old_get_view(self, view_id=view_id, view_type=view_type, **options)
    view = etree.fromstring(res['arch'])
    for tag in view.xpath("//button[@user_ids]"):
        users_str = tag.get('user_ids')
        user_ids = [int(i) for i in users_str.split(',')]
        if self._uid not in user_ids and self._uid != SUPERUSER_ID:
            tag.getparent().remove(tag)
    res['arch'] = etree.tostring(view)
    return res


# @api.model
# def get_view(self, view_id=None, view_type='form', **options):
#         """ get_view([view_id | view_type='form'])
#
#         Get the detailed composition of the requested view like model, view architecture.
#
#         The return of the method can only depend on the requested view types,
#         access rights (views or other records), view access rules, options,
#         context lang and TYPE_view_ref (other context values cannot be used).
#
#         :param int view_id: id of the view or None
#         :param str view_type: type of the view to return if view_id is None ('form', 'list', ...)
#         :param dict options: boolean options to return additional features:
#             - bool mobile: true if the web client is currently using the responsive mobile view
#             (to use kanban views instead of list views for x2many fields)
#         :return: composition of the requested view (including inherited views and extensions)
#         :rtype: dict
#         :raise AttributeError:
#
#             * if the inherited view has unknown position to work with other than 'before', 'after', 'inside', 'replace'
#             * if some tag other than 'position' is found in parent view
#
#         :raise Invalid ArchitectureError: if there is view type other than form, list, calendar, search etc... defined on the structure
#         """
#         self.browse().check_access('read')
#
#         result = dict(self._get_view_cache(view_id, view_type, **options))
#
#         node = etree.fromstring(result['arch'])
#         node = self.env['ir.ui.view']._postprocess_access_rights(node)
#         result['arch'] = etree.tostring(node, encoding="unicode").replace('\t', '')
#
#         return result


BM.default_get = default_get_new
BM.wkf_button_action = wkf_button_action
BM.wkf_action = wkf_action
BM.wkf_button_show_log = wkf_button_show_log
BM.wkf_button_reset = wkf_button_reset
BM.get_view = new_get_view
######################################################################


##############################
