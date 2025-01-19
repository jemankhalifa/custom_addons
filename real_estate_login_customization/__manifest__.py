{
    'name': 'Cafe Login Theme',
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
            'real_estate_login_customization/static/src/css/login_styles.css',
            '/real_estate_login_customization/static/src/img/back.jpg',
        ],
    },
    'installable': True,
    'application': False,
}

