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
            'login_tarzi_custom/static/src/css/login_styles.css',
            '/login_tarzi_custom/static/src/img/back_bg.png',
        ],
    },
    'installable': True,
    'application': False,
}

