# -*- coding: utf-8 -*-
{
    'name': "rod_account",

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
    'depends': ['base','account','l10n_bo_base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_journal.xml',
        'views/account_account.xml',
        'views/account_move.xml',
        'wizard/wizard_account_report.xml',
        'wizard/wizard_mayor_book.xml',
        'report/report.xml',
        'report/report_account_move_line.xml',
        'report/report_proof_payment.xml',
        'report/report_mayor_book.xml',
        'report/report_sums_balances.xml',
        'views/rod_account_menuitem.xml',

    ],
}

