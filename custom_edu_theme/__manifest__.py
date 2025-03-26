{
    'name': 'Educational Website Customizations',
    'version': '1.0',
    'summary': 'Modifications and improvements to the Net4X educational website',
    'description': 'The module adds features for registering visitors, joining courses, tracking progress, generating certificates, and customizing company colors and logo.',    'category': 'Website',
    'author': 'Tamadur Omer',
    'depends': ['website', 'website_sale', 'website_membership'],
    'data': [
        #'views/website_templates.xml',
        #'data/website_menus.xml',
        #'security/ir.model.access.csv',
    ],
    'assets': {
    'web.assets_frontend': [
        'custom_edu_theme/static/js/custom_scripts.js',
        'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.10.4/gsap.min.js',
        'custom_edu_theme/static/css/custom_styles.css',
       # 'custom_edu_theme/static/js/custom_scripts.js',
        #'custom_edu_theme/static/lottie/animation.json',
       # 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.10.4/gsap.min.js',  # إضافة GSAP
        #'https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.9.4/lottie.min.js',  # إضافة Lottie
    ],
    },
    'installable': True,
    'application': True,
}
