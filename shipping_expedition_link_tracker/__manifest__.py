# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Shipping Expedition Link Tracker',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'shipping_expedition', 'link_tracker'],
    'data': [
        'views/shipping_expedition.xml',
    ],
    'installable': True,
    'auto_install': False,    
}