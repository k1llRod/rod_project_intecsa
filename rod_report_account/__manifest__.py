# -*- coding: utf-8 -*-
{
    'name': "rod_report_account",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_account.xml',
        'report/report_account_move_line.xml',
        'report/report.xml',
        'wizard/wizard_account_report.xml',
        'views/rod_report_account_menuitem.xml',


    ],
}

