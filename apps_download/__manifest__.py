# -*- coding: utf-8 -*-
{
    "name": "Product Download for Appstore",
    "version": "10.0.0.0.1",
    "author": "BizzAppDev, AgentERP, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/apps-store",
    "license": "AGPL-3",
    "category": "Uncategorized",
    "depends": [
        'base',
        'website_sale_digital',
        'github_connector_odoo'
    ],
    "summary": "Product Download for Appstore",
    "data": [
        'views/product_template_view.xml',
        'data/cron_scheduler.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
