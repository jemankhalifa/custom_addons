
{
    'name': 'HR Expense Portal',
    'author': 'Net4X Innovation',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Custom Expense Portal for Employees',
    'depends': ['base', 'expense_portal'],
    'data': [
        'views/portal_dashboard.xml',
        'views/portal_expense_templates.xml',
        #'views/website_navbar.xml'

    ],
    'installable': True,
    'application': False,
}
