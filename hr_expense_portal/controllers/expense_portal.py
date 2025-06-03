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
        remaining_balance = 0.0
        if employee:
            remaining_balance = employee.get_remaining_balance() 
            
        return request.render("hr_expense_portal.portal_create_expense_form", {
            'employee_name': employee.name if employee else request.env.user.name,
            'remaining_balance': remaining_balance,
        })
    @http.route(['/my/expense/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def submit_expense(self, **post):
        employee = request.env.user.employee_id

        if employee:
            amount = float(post.get('amount', 0))
            date = post.get('date')
            note = post.get('note')
            uploaded_file = post.get('attachment')

            # احصل على الرصيد المتبقي من الموظف
            remaining_balance = float(post.get('remaining_balance', 0))

            # تحقق من أن المبلغ لا يتجاوز الرصيد المتبقي
            if amount > remaining_balance:
                return request.render("hr_expense_portal.portal_create_expense_form", {
                    'employee_name': employee.name,
                    'error_message': f"The amount exceeds your remaining balance ({remaining_balance:.2f}).",
                    'amount': amount,
                    'date': date,
                    'note': note,
                    'remaining_balance': remaining_balance,
                })

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
        employee = request.env.user.employee_id

        # حساب remaining_balance من موديل آخر (مثلاً من جدول current.balance.labor.lines)
        balance_line = request.env['current.balance.labor.lines'].sudo().search([
            ('employee_id', '=', employee.id)
        ], limit=1, order='id desc')

        remaining_balance = balance_line.remaining_balance if balance_line else 0.0
        employee_name = expense.employee_id.name
        amount = expense.amount
        date = expense.date
        note = expense.note
       
        return request.render('hr_expense_portal.edit_expense_template', {
            'expense': expense,
            'employee_name': employee_name,
            'amount': amount,
            'date': date,
            'note': note,
            'remaining_balance': remaining_balance,
        })
    @http.route('/my/expense/update', type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def update_expense(self, **post):
        expense = request.env['expense.portal'].sudo().browse(int(post.get('expense_id')))
        if expense.state != 'draft':
            return request.redirect('/my/expenses')

        amount = float(post.get('amount', 0))
        remaining_balance = float(post.get('remaining_balance', 0))
        date = post.get('date')
        note = post.get('note')

        # تحقق من أن المبلغ لا يتجاوز الرصيد المتبقي
        if amount > remaining_balance:
            employee = request.env.user.employee_id
            return request.render('hr_expense_portal.edit_expense_template', {
                'employee_name': employee.name,
                'error_message': f"The amount exceeds your remaining balance ({remaining_balance:.2f}).",
                'amount': amount,
                'date': date,
                'note': note,
                'remaining_balance': remaining_balance,
                'expense_id': expense.id,
            })

        expense.sudo().write({
            'amount': amount,
            'date': date,
            'note': note,
            'remaining_balance': remaining_balance,
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

    @http.route('/my/expense/create', type='http', auth='user', website=True)
    def create_expense_form(self, **kwargs):
        employee = request.env.user.employee_id

        # حساب remaining_balance من موديل آخر (مثلاً من جدول current.balance.labor.lines)
        balance_line = request.env['current.balance.labor.lines'].sudo().search([
            ('employee_id', '=', employee.id)
        ], limit=1, order='id desc')

        remaining_balance = balance_line.remaining_balance if balance_line else 0.0

        return request.render('hr_expense_portal.portal_create_expense_form', {
            'employee_name': employee.name,
            'remaining_balance': remaining_balance,
        })
