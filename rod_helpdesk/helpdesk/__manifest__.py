# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Helpdesk',
    'summary': 'Track, prioritize, and solve customer tickets',
    'description': """
    Long description of module's purpose
        """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base_setup',
        'mail',
        'utm',
        'rating',
        'web_tour',
        'resource',
        'portal',
        'digest',
    ],
    'data': [
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'data/digest_data.xml',
        'data/mail_activity_type_data.xml',
        'data/mail_message_subtype_data.xml',
        'data/mail_template_data.xml',
        'data/helpdesk_data.xml',
        'data/ir_cron_data.xml',
        'data/ir_sequence_data.xml',
        'views/helpdesk_ticket_views.xml',
        'report/helpdesk_ticket_analysis_views.xml',
        'report/helpdesk_sla_report_analysis_views.xml',
        'views/helpdesk_tag_views.xml',
        'views/helpdesk_ticket_type_views.xml',
        'views/helpdesk_stage_views.xml',
        'views/helpdesk_sla_views.xml',
        'views/helpdesk_team_views.xml',
        'views/digest_views.xml',
        'views/helpdesk_portal_templates.xml',
        'views/rating_rating_views.xml',
        'views/res_partner_views.xml',
        'views/mail_activity_views.xml',
        'views/helpdesk_templates.xml',
        'views/helpdesk_menus.xml',
        'wizard/helpdesk_stage_delete_views.xml',
    ],
    'post_init_hook': '_create_helpdesk_team',
    'assets': {
        'web.assets_backend': [
            'helpdesk/static/src/scss/helpdesk.scss',
            'helpdesk/static/src/css/portal_helpdesk.css',
            'helpdesk/static/src/components/**/*',
            'helpdesk/static/src/views/**/*',
            'helpdesk/static/src/js/tours/helpdesk.js',
        ],
        'web.qunit_suite_tests': [
            'helpdesk/static/tests/**/*',
        ],
    }
}
