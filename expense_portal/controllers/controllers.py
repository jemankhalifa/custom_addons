# controllers/controllers.py
from odoo import http
from odoo.http import request

class PortalExpense(http.Controller):

    @http.route(['/my/expenses/new'], type='http', auth='user', website=True)
    def portal_create_expense(self, **kwargs):
        return request.render('your_expense_module.portal_expense_form', {})

    @http.route(['/my/expenses/create'], type='http', auth='user', methods=['POST'], website=True)
    def portal_create_expense_post(self, **post):
        vals = {
            'name': post.get('name'),
            'amount': float(post.get('amount')),
            'description': post.get('description'),
            'employee_id': request.env.user.employee_id.id
        }
        request.env['your.expense.model'].sudo().create(vals)
        return request.redirect('/my/expenses')
