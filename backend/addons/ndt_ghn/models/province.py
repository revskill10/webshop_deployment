# -*- coding: utf-8 -*-

from odoo import api, fields, models
import re
import requests
# headers = ''
# headers = {'token': '81f253e7-e8da-11ea-84a7-3e05d9a3136e'}
# response = requests.post('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', 
#         headers=headers)
# print(response.json())



class Province(models.Model):
    _description = 'Province'
    _inherit = 'res.country.province'

    ghn_code = fields.Char()
    ghn_id = fields.Char()
    

    def ghn_province(self):

        headers = {'token': '81f253e7-e8da-11ea-84a7-3e05d9a3136e'}
        response = requests.post('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', 
                headers=headers)
        ghn_provinces = response.json()['data']
        print ("***ghn_provinces", type(ghn_provinces))
        for r in self.search([]):
            name = re.sub('tỉnh |thành phố |tp ','',r.name,flags= re.I)
            print ('**r.name', name)
            for ghn_item in ghn_provinces:
                ProvinceName = ghn_item['ProvinceName']
                print ('***ProvinceName', ProvinceName)
            # ghn_item = filter(lambda i: i['ProvinceName']==r.name, ghn_provinces)
                # ghn_item = list(ghn_item)
                if ProvinceName == name:
                    print ('***ProvinceName***',ProvinceName)
                    r.ghn_id = ghn_item['ProvinceID']
                    r.ghn_code = ghn_item['Code']
                    print ('**ghn_id**', r.ghn_id, r.ghn_code)



    
   