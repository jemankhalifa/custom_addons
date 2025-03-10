{
    'name': 'Custom Expense Portal',
    'sequence': -100,
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Custom Expense Portal for Employees',
    'depends': ['hr_expense','accountant'],
    'data': [
        'security/ir.model.access.csv',
        'security/expenses_group.xml',
        'views/custom_expense_views.xml',
        'views/current_balance_labor.xml',
    ],
    'installable': True,
    'application': True,
}