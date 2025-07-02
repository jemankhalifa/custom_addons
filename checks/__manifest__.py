# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Checks',
    'version': '18.0.1.0',
    'summary': 'Manage issuance and receipt of checks with tracking, reminders, and reporting.',
    'author': 'Net4X Innovation',
    'website': 'https://net4x-innovation.com/',
    'sequence': 10,
    'description': """
        Comprehensive Check Management
    
        This module provides complete functionality to manage checks in your organization:
        - Issue checks and track their lifecycle (draft, issued, sent).
        - Receive checks and manage their status (draft, received, deposited, cleared, bounced).
        - Automatic reminders for due or overdue checks via scheduled cron jobs.
        - Reconciliation status tracking with user access control.
        - Smart buttons linking related documents and activities.
        - Analytical dashboards for both issued and received checks.
        - Detailed PDF reports for issuing and receiving checks.
        - Wizards to assist in batch processing.
        - Full integration with Accounting and Communication (mail) modules.
    """,
    'category': 'Accounting',
    'depends': ['base', 'account', 'mail'],
    'data': [
        'views/check_issuance_views.xml',
        'views/check_receive_views.xml',
        'views/dashboard_receive_check.xml',
        'views/dashboard_issuing_check.xml',
        'data/check_sequence.xml',
        'reports/issurnce_report.xml',
        'reports/issurnce_report_action.xml',
        'data/cron_reminder.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'wizard/wizard_receive_views.xml',
        'wizard/wizard_issuance_views.xml',
        'reports/report_wizard_view.xml',
        'reports/report_wizard_action.xml',
        'wizard/wizard_issuance_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
