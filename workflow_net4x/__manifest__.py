{
    'name': 'Workflow Customization',
    'version': '18.0.1.0',
    'author': 'Net4X Innovation',
    'website': 'https://net4x-innovation.com/',
    'summary': """Advanced Workflow Enhancements and Tools for Odoo Users and Developers""",
    'Description': """ The wkf_powerful module is a utility toolkit for Odoo developers and power users 
        to streamline custom workflow creation and object state control. 
        It introduces reusable tools to manage record lifecycle actions such as 
        confirmations, validations, archiving, 
        and logging — without having to redefine them in every model.""",
    'category': 'Tools',
    'license': 'LGPL-3',
    'depends': ['purchase', 'calendar', 'base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/wkf_base_view.xml',
        'views/wkf_node_view.xml',
        'views/wkf_trans_view.xml',
        'views/wkf_log_trans_view.xml',
        'wizard/wizard_wkf_view.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
