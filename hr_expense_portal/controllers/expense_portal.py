from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import base64


class CustomPortalRedirect(CustomerPortal):

    @http.route('/my', type='http', auth="user", website=True)
    def custom_portal_home(self, **kw):
        if request.env.user.has_group('base.group_portal'):
            return request.redirect('/my/dashboard')
        return super().home(**kw)

class ExpensePortal(http.Controller):

    # @http.route(['/my/hr/dashboard'], type='http', auth="user", website=True)
    # def hr_dashboard(self, **kw):
    #     return request.render('hr_expense_portal.add_hr_portal_card')

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
            amount = post.get('amount')
            date = post.get('date')
            note = post.get('note')
            uploaded_file = post.get('attachment')

            expense = request.env['expense.portal'].sudo().create({
                'employee_id': employee.id,
                'amount': amount,
                'date': date,
                'note': note,
                'state': 'draft',
            })

            if uploaded_file:
                file_content = uploaded_file.read()
                file_name = uploaded_file.filename

                request.env['ir.attachment'].sudo().create({
                    'name': file_name,
                    'type': 'binary',
                    'datas': base64.b64encode(file_content).decode('utf-8'),
                    'res_model': 'expense.portal',  
                    'res_id': expense.id,             
                    'mimetype': uploaded_file.content_type,
                })
            if post.get('action') == 'submit':
                expense.action_submit()

        return request.redirect('/my/expenses')

    @http.route('/my/expense/edit/<int:expense_id>', type='http', auth='user', website=True)
    def edit_expense(self, expense_id, **kw):
        expense = request.env['expense.portal'].sudo().browse(expense_id)
        if expense.state != 'draft':
            return request.redirect('/my/expenses')  
        employee_name = expense.employee_id.name
        return request.render('hr_expense_portal.edit_expense_template', {
            'expense': expense,
            'employee_name': employee_name,
        })
    @http.route('/my/expense/update', type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def update_expense(self, **post):
        expense = request.env['expense.portal'].sudo().browse(int(post.get('expense_id')))
        if expense.state != 'draft':
            return request.redirect('/my/expenses')

        expense.sudo().write({
            'amount' : post.get('amount'),
            'date' : post.get('date'),
            'note' : post.get('note'),
        })
        uploaded_file = post.get('attachment')

        if uploaded_file:
            file_content = uploaded_file.read()
            file_name = uploaded_file.filename

            request.env['ir.attachment'].sudo().create({
                'name': file_name,
                'type': 'binary',
                'datas': base64.b64encode(file_content).decode('utf-8'),
                'res_model': 'expense.portal',  
                'res_id': expense.id,             
                'mimetype': uploaded_file.content_type,
            })
        if post.get('action') == 'submit':
            expense.action_submit()
       
        return request.redirect('/my/expenses')

