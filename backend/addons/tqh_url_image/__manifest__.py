{
    'name': 'NDT URL image',
    'version': '1.0',
    'category': 'Product',
    'sequence': 1,
    'summary': 'API',
    'description': """Thêm trường ảnh Url """,
    'depends': ['base', 'product','ndt_cloud_attachment_product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/product_product.xml',
        'views/product_category.xml',
        'views/url_image.xml'
    ],
    'installable': True,
    'auto_install': False,
}
