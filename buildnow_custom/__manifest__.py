{
    'name': 'Buildnow custom code',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Manage properties, sales, leases, tenants, and agents',
    'description': """
Real Estate Management Module
This module allows real estate agencies, property managers, and landlords to manage their properties, agents, tenants, and leases easily.

""",
    'author': 'Net4x Innovation',
    'website': 'https://net4x-innovations.com',
    'depends': ['base','web','crm','stock','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/deals_view.xml',
   
      
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