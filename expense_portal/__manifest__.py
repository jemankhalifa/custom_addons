{
    'name': 'Custom Expense Portal',
    'sequence': -100,
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Custom Expense Portal for Employees',
    'depends': ['hr_expense'],
    'data': [
        'views/custom_expense_views.xml',
    ],
    'installable': True,
    'application': True,
}