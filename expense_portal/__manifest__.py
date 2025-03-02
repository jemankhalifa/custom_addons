{
    'name': 'Expense Portal',
    'sequence': -100,
    'version': '1.0',
    'summary': 'Manage employee expenses',
    'description': 'A portal for employees to submit and track expenses.',
    'author': 'Your Name',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/expense_views.xml',
    ],
    'installable': True,
    'application': True,
}