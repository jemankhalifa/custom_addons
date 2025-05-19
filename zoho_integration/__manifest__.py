# -*- coding: utf-8 -*-
{
    'name': "Zoho Integration",
    'summary': """Connects Odoo with Zoho""",
    'description': """Connects Odoo with Zoho Books""",
    'author': "Net4X",
    'website': "https://edu.net4x-innovation.com/",
    # https://www.zoho.com/books/api/v3/introduction/#organization-id
    'category': 'Technical',
    'version': '18.0.1.0',
    'depends': ['base',
                'product',
                'purchase'],

    'data': [
        'data/crons.xml',
        'security/ir.model.access.csv',
        'views/partners_view.xml',
        'views/purchase_order_view.xml',
        # 'views/item_view.xml',
        'views/menus.xml',
    ],
    'demo': [
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
