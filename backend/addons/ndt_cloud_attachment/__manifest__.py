{
    'name': 'NDT cloud attachment',
    'version': '1.0',
    'category': 'Product',
    'sequence': 1,
    'summary': 'API',
    'description': """Thêm trường ảnh Url """,
    'depends': ['base', 'product','stock'],
    'data': [
        # 'data/cronjob_data.xml',
        # 'security/ir.model.access.csv',
        # 'views/product_template.xml',
        # 'views/product_product.xml',
        'views/setting.xml',
        # 'views/fields.xml',

    ],
    "external_dependencies": {"python": ["cloudinary"]},
    'installable': True,
    'auto_install': False,
}
