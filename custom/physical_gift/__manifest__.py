# -*- coding: utf-8 -*-
{
    'name': 'Physical Gift Management',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Quản lý quà tặng vật lý',
    'description': """
        Module quản lý quà tặng vật lý với các tính năng:
        - Quản lý chương trình quà tặng
        - Quản lý danh mục quà tặng
        - Quản lý thương hiệu đối tác
        - Quản lý quà tặng vật lý
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base',
        'mail',
        'product',
        'sale',
        'account',
    ],
        'data': [
        'security/ir.model.access.csv',
        'data/physical_gift_demo_data.xml',
                'views/physical_gift_item_views.xml',
                'views/physical_gift_brand_views.xml',
                'views/physical_gift_category_views.xml',
                'views/physical_gift_program_enhanced_views.xml',
                'views/physical_gift_supplier_views.xml',
                'views/physical_gift_shipping_unit_views.xml',
                'views/physical_gift_import_views.xml',
                'views/physical_gift_order_views.xml',
                'views/physical_gift_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'physical_gift/static/src/css/physical_gift.css',
            'physical_gift/static/src/css/physical_gift_brand.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 