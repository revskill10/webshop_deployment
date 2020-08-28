{
    'name': 'NDT TQH API',
    'version': '1.0',
    'category': 'Tools',
    'sequence': 1,
    'summary': 'API',
    'description': """""",
    'depends': ['base', 'product', 'sale'],
    'data': [
        'views/sale_order.xml',
        'data/cronjob_data.xml'
    ],

    "external_dependencies": {"python": ["requests"]},
    'installable': True,
    'auto_install': False,
}
