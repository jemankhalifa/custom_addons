# """"
# The Expense Portal is a custom Odoo module designed to streamline the process of submitting,
# tracking, and managing employee expenses for small businesses.
# It provides employees with a user-friendly interface to submit their expenses,
# allows managers to review and approve/reject expenses, and generates PDF reports for
# record-keeping and auditing purposes.
# """"

{
    'name': 'Custom Expense Portal',
    'author': 'Net4X Innovation',
    'website': 'https://net4x-innovation.com/',
    'version': '18.0.1.0',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'summary': 'Submit and manage employee expenses with approvals and reports',
    'description': """The Expense Portal is a custom Odoo module designed to streamline the process of submitting,
    tracking, and managing employee expenses for small businesses. It provides employees with a user-friendly interface
    to submit their expenses, allows managers to review and approve/reject expenses, and generates PDF reports for
    record-keeping and auditing purposes.""",
    'depends': ['hr_expense', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'security/expenses_group.xml',
        'views/custom_expense_views.xml',
        'views/current_balance_labor.xml',
        'report/current_balance_template.xml',
        'report/report_action.xml',
    ],
    'installable': True,
    'application': True,
}
