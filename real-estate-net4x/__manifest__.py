{
    'name': 'Real Estate Net4x',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Manage properties, sales, leases, tenants, and agents',
    'description': """
Real Estate Management Module
This module allows real estate agencies, property managers, and landlords to manage their properties, agents, tenants, and leases easily.

""",
    'author': 'Net4x Innovation',
    'website': 'https://net4x-innovations.com',
    # 'depends': ['crm','sale_renting_crm','industry_real_estate'],
    # 'depends': ['sale_crm','sale_renting','industry_real_estate'],
    'depends': ['sale_renting_crm'],
    # 'depends': ['base','web','crm','stock','sale'],
    'data': [
        'data/crm_stages.xml',
        'data/account_analytic_plan.xml',
        'data/property_stages.xml',

        'security/real_estate_security.xml',
        'security/ir.model.access.csv',
        'views/main_configs_views.xml',
        'views/real_estate_contract_view.xml',
        'views/real_estate_quotation.xml',
        'views/crm_lead_view.xml',
        'views/real_estate_stage_views.xml',
        # 'views/partner_view.xml',
        'views/product_template_views.xml',
        'views/real_estate_view.xml',
        'views/ir_filters.xml',
        'wizard/realestate_lead_wizard_view.xml',
        'views/real_estate_menus.xml'
      
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