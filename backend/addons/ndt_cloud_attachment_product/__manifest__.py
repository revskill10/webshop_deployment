{
    'name': 'ndt_cloud_attachment_product',
    'version': '1.0',
    'category': 'Product',
    'sequence': 1,
    'summary': 'API',
    'description': """Thêm trường ảnh Url """,
    'depends': ['base', 'product','stock','ndt_cloud_attachment'],
    'data': [
        'data/data_fields.xml',
        # 'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/product_product.xml',
        # 'views/setting.xml',
    ],
    "external_dependencies": {"python": ["cloudinary"]},
    'installable': True,
    'auto_install': False,
}
