# -*- coding: utf-8 -*-
{
    'name': "tourism",

    'summary': "tourism",

    'description': "tourism",

    'author': "Saafan  Solutions",
    'website': "https://theantmate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
#     'version': '17.0',
#     'version': '1.3',
    'version': '1.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'sale', 'sale_management', 'crm', 'account', 'hr', 'purchase'],
    'license': 'OPL-1',
    # always loaded
    'data': [
        'wizard/wizard_view.xml',
        'views/menu.xml',
        'views/sales_to_invoice.xml',
        'reports/report.xml',
        'views/sales_to_purchase.xml',
        'security/ir.model.access.csv',
        'views/sale_order_line_search_view.xml'
    ],
}
