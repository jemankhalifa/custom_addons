from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class CustomPortalRedirect(CustomerPortal):

    @http.route('/my', type='http', auth="user", website=True)
    def custom_portal_home(self, **kw):
        if request.env.user.has_group('base.group_portal'):
            return request.redirect('/my/dashboard')
        return super().home(**kw)

class ExpensePortal(http.Controller):

    @http.route(['/my/dashboard'], type='http', auth="user", website=True)
    def dashboard_page(self, **kw):
        return request.render('hr_expense_portal.portal_dashboard_template')

    @http.route(['/my/expenses'], type='http', auth="user", website=True)
    def portal_my_expenses(self, **kw):
        expenses = request.env['expense.portal'].sudo().search([
            ('employee_id.user_id', '=', request.uid)
        ])
        return request.render('hr_expense_portal.portal_my_expenses', {
            'expenses': expenses,
        })

    @http.route(['/my/expense/create'], type='http', auth="user", website=True)
    def create_expense_form(self, **kw):
        employee = request.env.user.employee_id
        return request.render("hr_expense_portal.portal_create_expense_form", {
            'employee_name': employee.name if employee else request.env.user.name,
        })

    @http.route(['/my/expense/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def submit_expense(self, **post):
        employee = request.env.user.employee_id
        if employee:
            request.env['expense.portal'].sudo().create({
                'employee_id': employee.id,
                'amount': post.get('amount'),
                'date': post.get('date'),
                'name': post.get('notes'),
                
                
            })
        return request.redirect('/my/expenses')










    # @http.route(['/my/expenses'], type='http', auth="user", website=True)
    # def portal_my_expenses(self, **kw):
    #     expenses = request.env['hr.expense'].sudo().search([
    #         ('employee_id.user_id', '=', request.uid)
    #     ])
    #     return request.render('hr_expense_portal.portal_my_expenses', {
    #         'expenses': expenses,
    #     })

    # @http.route(['/my/expenses/request'], type='http', auth="user", website=True)
    # def portal_new_expense(self, **kw):
    #     return request.render('hr_expense_portal.portal_new_expense_form')

    # @http.route(['/my/expenses/submit'], type='http', auth="user", website=True, methods=['POST'])
    # def portal_submit_expense(self, **post):
    #     user = request.env.user
    #     employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)

    #     request.env['hr.expense'].sudo().create({
    #         'name': post.get('description'),
    #         'total_amount': float(post.get('amount')),
    #         'employee_id': employee.id,
    #     })
    #     return request.redirect('/my/expenses')
