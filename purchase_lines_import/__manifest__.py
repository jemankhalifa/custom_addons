################################################

{
    'name': 'Purchase Lines Import',
    'version': '18.0.1.0',
    'author': 'Net4X Innovation',
    'website': 'https://net4x-innovation.com/',
    'summary': """Custom Feature to allow import purchase order lines from excel files""",
    'Description': """ Allow you to import long list of purchases items from excel file 
        and create a PO by selecting a vendor, date and all products lines imported""",
    'category': 'Purchase',
    'license': 'LGPL-3',
    'depends': ['purchase', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_lines_migration_view.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
