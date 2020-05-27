# -*- coding: utf-8 -*-
{
    'name': 'Shipping Expedition Link Tracker Custom',
    'version': '10.0.1.0.0',
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'shipping_expedition', 'shipping_expedition_link_tracker', 'link_tracker'],
    'data': [
        'data/ir_cron.xml',
    ],
    'installable': True,
    'auto_install': False,
}