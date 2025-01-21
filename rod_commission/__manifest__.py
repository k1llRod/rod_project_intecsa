# -*- coding: utf-8 -*-
{
    'name': "rod_commission",

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
    'depends': ['sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/commission_payment.xml',
        'views/seller_commission.xml',
        'views/sale_order.xml',
        'views/res_config_setting.xml',
        'wizard/wizard_commission_payment.xml',
        'report/payment_receipt_pdf.xml',
        'report/report.xml',

    ],
}

