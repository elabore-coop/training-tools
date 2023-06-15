# -*- coding: utf-8 -*-

{
    "name": 'Learning Base',
    "version": "16.0.0.0.0",
    "depends": [
        #'__export__',
        'base',
        'event',
        'sale',
        'product',
        'website',
        'website_sale',
        'event_sale',
        'partner_firstname',
        'product',
        'website_event_sale',
        'purchase',
    ],
    "author": "Nicolas JEUDY, Odoo Community Association (OCA)",
    "installable": True,
    "data": [
        'security/learning_security.xml',
        'security/ir.model.access.csv',
        'ir_actions_act_window_records.xml',
        'ir_ui_menu_records.xml',
        'ir_module_category_records.xml',
        'views/product_template.xml',
        'views/event_event.xml',
        'views/res_company.xml',
        'views/res_partner.xml',
        'views/template.xml',
    ],
}
