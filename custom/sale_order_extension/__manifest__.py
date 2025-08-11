{
    'name': 'Sale Order Extension',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Extend sale order with additional information fields',
    'description': """
        Module to extend Sale Order functionality with:
        - Additional PO information fields (PO Path, PO Number)
        - Delivery and receiver information
        - Order classification and status
        - Notes and additional information
        - Organized interface with tabs
    """,
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
