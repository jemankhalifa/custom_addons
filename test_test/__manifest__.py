{
    'name': 'Test Net4x',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Manage properties, sales, leases, tenants, and agents',
    'description': """


""",
    'author': 'Net4x Innovation',
    'website': 'https://net4x-innovations.com',
    'depends': ['base','web','crm','stock','sale'],
    'data': [
        #'security/real_estate_security.xml',
        'data/sequence.xml',    
        'security/ir.model.access.csv',
        'views/view.xml',
        
      
    ],
     'assets': {
        'web.assets_backend': [
          
        ],
    },
'license': 'LGPL-3',

    'installable': True,
    'auto_install' : False,
    'application': True,

}