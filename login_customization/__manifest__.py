{
    'name': 'Net4x Login Theme',
    'version': '1.0',
    'author': 'Tamadur',
    'category': 'Website',
    'summary': 'Customizes the login page design and theme.',
    'depends': ['web','website'],
    'data': [
        'views/login_template.xml',
        'views/assets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'login_customization/static/src/css/login_styles.css',
            'login_customization/static/src/img/cafe_bg2.jpeg',
        ],
    },
    'installable': True,
    'application': False,
}

