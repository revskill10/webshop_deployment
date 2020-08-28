# -*- coding: utf-8 -*-
{
    
    'name': "Blog content",
    'summary':"Blog content",
    'version': '0.1',
    # 'category': 'sale,stock',
    'website': "http://www.vidoo.vn",
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base','website_blog'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/blog_post.xml',
        # 'views/templates.xml',
    ],
    "external_dependencies": {"python": ["unidecode"]},
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}