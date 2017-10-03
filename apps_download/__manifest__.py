# -*- coding: utf-8 -*-
{
    "name": "Product Download for Appstore",
    "version": "10.0.0",
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
    "description": """
    Product Download with all dependent modules
    """,
    'images': [],
    "init_xml": [],
    "data": [
        'views/product_template_view.xml',
        'data/cron_scheduler.xml'
    ],
    'demo_xml': [
    ],
    'test':[
    ],
    'installable': True,
    'active': False,
    'auto_install': False,
    'application':False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
