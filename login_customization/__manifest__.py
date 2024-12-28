{
    'name': 'Login Page Customization',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Website',
    'summary': 'Customizes the login page design and theme.',
    'depends': ['web'],
    'data': [
        'views/login_template.xml',
        'views/assets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'login_customization/static/src/css/login_styles.css',
            'http://localhost:8069/login_customization/static/src/img/cafe_bg2.jpeg',
        ],
    },
    'installable': True,
    'application': False,
}

