from odoo import api, SUPERUSER_ID

"""Create the purchase_order_line_id field if it doesn't exist"""


def migrate_purchase_line_field(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    Model = env['ir.model.fields']

    if not Model.search([
        ('name', '=', 'purchase_order_line_id'),
        ('model', '=', 'account.move.line')
    ]):
        Model.create({
            'name': 'purchase_order_line_id',
            'model_id': env.ref('account.model_account_move_line').id,
            'field_description': 'Purchase Order Line (Custom)',
            'ttype': 'many2one',
            'relation': 'purchase.order.line.data',
            'store': True,
            'index': True,
        })
