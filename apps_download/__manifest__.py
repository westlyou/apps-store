# -*- coding: utf-8 -*-
# Copyright 2013-2017 BizzAppDev - Ruchir Shukla <ruchir@bizzappdev.com>
# Copyright 2013-2017 AgentERP - Georg Notter <georg.notter@agenterp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Download for Appstore",
    "version": "10.0.1.0.0",
    "author": "BizzAppDev, AgentERP, Elico Corp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/apps-store",
    "license": "AGPL-3",
    "category": "Sales",
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
