# -*- coding: utf-8 -*-
{
    'name': "CRM Auto Assign",

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
    'depends': ['base', 'sale', 'sale_management', 'crm', 'account'],
    'license': 'OPL-1',
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/prob.xml',
        'views/crm_lead.xml',

    ],
}
