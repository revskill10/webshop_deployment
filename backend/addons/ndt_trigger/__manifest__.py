# -*- coding: utf-8 -*-
{
    
    'name': "NDT Trigger",
    'summary':"NDT Trigger",
    'version': '0.1',
    'website': "http://www.vidoo.vn",
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base','product','stock','sale_management','attrs_json','ndt_bestseller','ndt_blog_content',
    'ndt_brand_url_image','ndt_seo_url','tqh_api','tqh_url_image'],
    'data': [
        'data/cronjob_data.xml',
        'security/ir.model.access.csv',
        'views/trigger.xml',
    ],
    # "external_dependencies": {"python": ["unidecode"]},
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}