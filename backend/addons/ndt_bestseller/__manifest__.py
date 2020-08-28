# -*- coding: utf-8 -*-
{
    
    'name': "NDT Best Seller",
    'summary':"NDT Best Seller",
    'version': '0.1',
    'website': "http://www.vidoo.vn",
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base','product','stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/ndt_bestseller.xml',
    ],
    "external_dependencies": {"python": ["unidecode"]},
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}