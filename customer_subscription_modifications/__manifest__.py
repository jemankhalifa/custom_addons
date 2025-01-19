{
    'name': 'Customer Subscription Modifications',
    'version': '1.0',
    'author': 'Tamadur Omer Albasheer Ali',
    'category': 'Custom',
    'summary': 'Adds custom fields and print subscriber card feature.',
    'depends': ['base', 'contacts'],
    'data': [
        'views/partner_inherit.xml',
        'report/subscriber_card.xml',
        'report/paperformat.xml',
    ],
    'installable': True,
    'application': True,
}

