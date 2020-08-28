# -*- coding: utf-8 -*-
{
    
    'name': "Seo Order request",
    'summary':"Seo Order request",
    'version': '0.1',
    'website': "http://www.vidoo.vn",
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sor.xml',
    ],
    "external_dependencies": {"python": ["unidecode"]},
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}