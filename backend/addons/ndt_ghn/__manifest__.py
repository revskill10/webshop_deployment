# -*- coding: utf-8 -*-
{
    
    'name': "NDT GHN",
    'summary':"NDT GHN",
    'version': '0.1',
    'website': "http://www.vidoo.vn",
    'author': "Nguyen Duc Tu",
    "license": "AGPL-3",
    'depends': ['base','as_vn_address'],
    'data': [
        'data/cronjob_data.xml',
        'views/province.xml',
        # 'security/ir.model.access.csv',
    ],
    "external_dependencies": {"python": ["requests"]},
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}