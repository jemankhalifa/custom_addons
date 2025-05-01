# -*- coding: utf-8 -*-
{
    'name': "Installments",
    'summary': "Calculation of customer installments",
    'description': """This module is allows you to manage customer installment plans for product purchases. 
                You can define payment schedules based on total amount, start date, and installment frequency (weekly, monthly, annually). 
                The module auto-generates installment lines and provides automated reminders or processing through scheduled actions (cron jobs). 
                It helps track due payments and updates payment status seamlessly.""",

    'author': "Net4X Innovation",
    'version': '18.0.1.0',
    'category': 'Accounting',
    'depends': ['base',
                'mail',
                'product',
                'account'],
    'data': [
        'data/cron_installments.xml',
        'data/data.xml',
        'data/email_template_installment.xml',
        'security/ir.model.access.csv',
        'views/customer_installment_views.xml',
        'views/deposit_installment_view.xml',
    ],
    'sequence': -90,
    'application': True,
    'installable': True,
    'auto_install': False,
}
