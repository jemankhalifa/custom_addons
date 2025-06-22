# -*- coding: utf-8 -*-
{
    'name': "Installments",
    'version': '18.0.1.0',
    'author': "Net4X Innovation",
    'website': 'https://net4x-innovation.com/',
    'license': 'LGPL-3',
    'summary': "Calculation of customer installments",
    'description': """This module is allows you to manage customer installment plans for product purchases. 
                You can define payment schedules based on total amount, start date, and installment frequency (weekly, monthly, annually). 
                The module auto-generates installment lines and provides automated reminders or processing through scheduled actions (cron jobs). 
                It helps track due payments and updates payment status seamlessly.""",
    'category': 'Accounting',
    'depends': ['base', 'mail', 'product', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/customer_installment_views.xml',
        'views/deposit_installment_view.xml',
        'data/cron_installments.xml',
        'data/data.xml',
        'data/email_template_installment.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
