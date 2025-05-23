################################################

{
    'name': 'Purchase Lines Import',
    'summary': """Custom Feature to allow import purchase order lines from excel files""",
    'Description': """ Allow you to import long list of purchases items from excel file 
        and create a PO by selecting a vendor, date and all products lines imported""",

    'version': '18.0.1.0',
    'category': 'Purchase',
    'author': 'Eman Khalifa',
    'licence': 'AGPL',
    'website': 'https://www.emankhalifa.com',
    'depends': ['purchase', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_lines_migration_view.xml',
    ],
    'sequence': 3,
    'application': False,
    'installable': True,
    'auto_install': False,
}
