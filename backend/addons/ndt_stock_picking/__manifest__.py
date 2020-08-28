{
    'name': 'NDT STOCK PICKING',
    'version': '1.0',
    'category': 'Tools',
    'sequence': 1,
    'summary': 'API',
    'description': """""",
    'depends': ['base','delivery'],
    'data': [
        'views/stock_picking.xml',
        'views/sale_order_line.xml',
    ],

    "external_dependencies": {"python": ["requests"]},
    'installable': True,
    'auto_install': False,
}
