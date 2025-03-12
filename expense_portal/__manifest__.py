{
    'name': 'Custom Expense Portal',
    'author': 'Net4X Innovation',
    'sequence': -100,
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Custom Expense Portal for Employees',
    'depends': ['hr_expense',
                'account'
                ],
    'data': [
        'security/ir.model.access.csv',
        'security/expenses_group.xml',
        'views/custom_expense_views.xml',
        'views/current_balance_labor.xml',
        'report/expense_portal_template.xml',
        'report/report_action.xml',
    ],
    'installable': True,
    'application': True,
}
