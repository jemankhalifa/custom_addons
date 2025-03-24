{
    'name': 'Check Printing Management',
    'author': 'Net4X Innovation',
    'sequence': -99,
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Manage check payments',
    'depends': ['account',
                'mail'
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/check_layout_views.xml',
        'views/check_layout_wizard_view.xml',
        'views/account_payment_views.xml',
        'report/report_check_template.xml',
        'report/report_action.xml',
    ],
    'installable': True,
    'application': True,
}
