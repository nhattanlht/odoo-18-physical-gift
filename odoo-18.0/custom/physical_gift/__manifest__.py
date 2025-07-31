# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Physical Gift',
    'version': '1.0',
    'summary': 'Quản lý chương trình quà tặng vật lý',
    'sequence': 10,
    'description': """
Physical Gift Management
=======================
Module quản lý chương trình quà tặng vật lý với các tính năng:
- Quản lý danh sách chương trình
- Tìm kiếm và lọc chương trình
- Xuất dữ liệu
- Thêm và cập nhật chương trình
    """,
    'category': 'Sales',
    'website': 'https://www.odoo.com',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/physical_gift_security.xml',
        'security/ir.model.access.csv',
        'data/physical_gift_data.xml',
        'views/physical_gift_views.xml',
        'views/physical_gift_menus.xml',
    ],
    'demo': [
        'data/physical_gift_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'physical_gift/static/src/css/physical_gift.css',
            'physical_gift/static/src/js/physical_gift.js',
        ],
    },
} 