{
    'name': 'Accounting Login Theme',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Website',
    'summary': 'Customizes the login page design and theme.',
    'depends': ['web','website'],
    'data': [
        'views/login_template.xml',
        'views/assets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'login_accounting_customization/static/src/css/login_styles.css',
            '/login_accounting_customization/static/src/img/account_bg.png',
        ],
    },
    'installable': True,
    'application': False,
}

