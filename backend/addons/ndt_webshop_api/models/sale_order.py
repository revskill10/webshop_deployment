# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
import json
from datetime import datetime
from time import sleep
def get_hasura_data(data):
    url = 'https://vast-beetle-97.hasura.app/v1/graphql'
    headers = {'x-hasura-admin-secret': 'satavan', 'content-type': 'application/json', 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    count_fail = 0
    while 1:
        try:
            request = requests.post(url, json=data, headers=headers)
            return request.json()
        except Exception as e:
            count_fail +=1
            print ('loi khi get html',e)
            sleep(5)
            if count_fail ==5:
                raise ValueError(u'Lỗi get html')
            
            
query_hasura ={'query': '''{
  sale_order_requests(
      limit:500,
      offset:%s,
    where:{
      _and:[{
        is_complete:{
          _eq:false
        }
      }, {
      tenant:{
        _eq:"vst"
      }
    }]
    }
  ){
    id
    user_id
    user_info
    order_info
    created_at
  }
}'''
}
LIMIT = 50
QUERY_OFFSET  = '''{
  sale_order_requests(
      limit:%s,
      offset:%s,
    where:{
      _and:[{
        is_complete:{
          _eq:false
        }
      }, {
      tenant:{
        _eq:"vst"
      }
    }]
    }
  ){
    id
    user_id
    user_info
    order_info
    created_at
  }
}'''
# data_hasura ={'query': '''{
#   sale_order_requests(
#     where:{
#       _and:[{
#       tenant:{
#         _eq:"vst"
#       }
#     }]
#     }
#   ){
#     id
#     user_id
#     user_info
#     order_info
#     created_at
#   }
# }'''
# }



query_update = '''mutation($completed_at:timestamptz!,$ids:[uuid!]!){
  update_sale_order_requests(
    _set:{
      is_complete:true,
      completed_at:$completed_at,
    },
    where:{
      id:{
        _in:$ids
      }
    }
  ){
    affected_rows
  }
}'''



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    hasura_soid = fields.Char()

    def tach_so(self, user_info, order_info, original_so_id):
        phone = user_info.get('phone')
        user_id = user_info['user_id']
        phone = '0' + str(phone[3:])
        company_order_item_dict = {}

        for order_item in  order_info:
            company_id = order_item['company_id']
            company_order_item = company_order_item_dict.setdefault(company_id,[])
            company_order_item.append(order_item)
        
        
        email = user_info['email']
        city = user_info['state']
        street = user_info['address']
        name = ''
        if user_info.get('first_name'):
            name = name + user_info.get('first_name')
        if user_info.get('last_name'):
            name = name + user_info.get('last_name')

        user_id = 1
        for company_id, company_order_items in company_order_item_dict.items(): 
            # partner = request.env['res.partner'].sudo().search([('phone', '=', phone), ('company_id', '=', company_id)], limit=1)
            partner = self.env['res.partner'].sudo().search([
                ('user_id', '=', user_id),
                ('company_id', '=', company_id),
                ('type', '=', 'contact'),
                ], limit=1)
            if not partner:
                data_partner = {
                    'name': name,
                    'phone': phone,
                    'company_id': company_id,
                    'user_id':user_id
                }
                if email:
                    data_partner.update({
                            'email': email
                        })

                if city:
                    data_partner.update({
                            'city': city
                        })
                
                if street:
                    data_partner.update({
                            'street': street
                        })
                partner = partner.create(data_partner)
                is_create_partner = True
            else:
                is_create_partner = False

            shipping_partner = self.env['res.partner'].sudo().search([
                ('parent_id', '=', partner.id), 
                ('company_id', '=', company_id), 
                ('street', '=', street),
                ('city', '=', city),
                ('type','=','delivery'),
                ('user_id','=',user_id)


            ], limit=1)

            if not shipping_partner:
                shipping_partner = self.env['res.partner'].sudo().create({
                    'parent_id': partner.id,
                    'company_id':company_id,
                    'street': street,
                    'city': city,
                    'phone': phone,
                    'name':'to: ' + name,
                    'type':'delivery',
                    'email':email,
                    'user_id':user_id,
                })
                is_shipping_partner_create = True
            else:
                is_shipping_partner_create = False
            so_data = {
                'partner_id': shipping_partner.id,
                'company_id': company_id,
                'hasura_soid':original_so_id,
            } 
            
            sale_order = self.env['sale.order'].sudo().create(so_data)
            
            for item in company_order_items:
                so_line_data = {
                                        'product_id': item['id'],
                                        'product_id': 1,
                                        'product_uom_qty': float(item['qty']),
                                        'price_unit': float(item['price']),
                                        'discount': float(item['discount']),
                                        'order_id': sale_order.id,
                                    }
                sale_order_line = self.env['sale.order.line'].sudo().create(so_line_data)
            self.env.cr.commit()
            return sale_order

    def place_order_cronjob(self):
      self._place_order_cronjob()
    def place_order_cronjob1(self):
      print ('***place_order_cronjob1**')
      self._place_order_cronjob(1)
    def place_order_cronjob2(self):
      print ('***place_order_cronjob2**')
      self._place_order_cronjob(2)
    def place_order_cronjob3(self):
      print ('***place_order_cronjob3**')
      self._place_order_cronjob(3)
    def place_order_cronjob4(self):
      print ('***place_order_cronjob4**')
      self._place_order_cronjob(4)
    def _place_order_cronjob(self, i=0):
        count_down = 1
        while count_down:
            count_down -=1
            for i_i in range(1):
                print ("tim kiem so chua complete")
                offset = i*LIMIT
                print ('***offset***', offset)
                query_hasura_post = {'query': QUERY_OFFSET%(LIMIT,offset)}
                rs = get_hasura_data(query_hasura_post)
                hasura_sos = rs['data']['sale_order_requests']
                if len(hasura_sos)==0:
                  print ('hết đơn hàng')
                many_sale_orders = []
                so_hasura_ids = []
                for data in hasura_sos:
                    sale_orders = []
                    original_so_id = data['id']
                    user_info = data.get('user_info')
                    order_info = data.get('order_info')
                    so = self.tach_so(user_info, order_info, original_so_id)
                    sale_orders.append(so.id)
                    so_hasura_ids.append(original_so_id)
                    many_sale_orders.append(sale_orders)
                update_data_hasura = {'query':query_update,'variables':{ 'ids':so_hasura_ids, 'completed_at': str(datetime.now())}}
                mutation_rs = get_hasura_data(update_data_hasura)
                
                print (many_sale_orders, mutation_rs)


