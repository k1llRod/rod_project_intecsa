# -*- coding: utf-8 -*-
{
    'name': "rod_purchase",

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
    'depends': ['base','purchase','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_move_line.xml',
        'views/stock_quant.xml',
        'views/purchase_order.xml',
        # 'views/stock_move_line.xml',
    ],
    # only loaded in demonstration mode
}

