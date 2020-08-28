# -*- coding: utf-8 -*-
from json import dumps
import json
import ast
from random import choice
from odoo import http
from odoo.http import request, Response
import traceback
import logging


_logger = logging.getLogger(__name__)

class ResPartnerAPI(http.Controller):

    @http.route('/api/user/create', type='json', auth='none', methods=['POST'], csrf=False)
    def create_user(self, **data):
        print ('create User...')

        try:
            data_request =  request.httprequest.data
            data_request = data_request.decode("UTF-8")
            data_request = json.loads(data_request)
            company = request.env['res.company'].sudo().create({
                'name':data_request['company_name'],
                'parent_id':1,

            })
            company_id = company.id

            user_seller = request.env['res.users'].sudo().create({
                'name':data_request['user_name'],
                'login':data_request['email'],
                'password':data_request['password'],
                'company_ids':False,
                'company_id':company_id,
                'phone':data_request['phone'],
                'email':data_request['email'],
                
            })
            return json.dumps({
                'code': 200,
                'message': 'success',
                'user_seller.id': user_seller.id,
                'company_id':company_id,
            })

        except:

            return json.dumps({
                'code': 500,
                'message': 'ndt internal fail',
                'detail': str(traceback.format_exc()),
            })

    @http.route('/api/order/create', type='json', auth='none', methods=['POST'], csrf=False)
    def create_order(self, **data):
        try:
            # print('**request.httprequest.QUERY_STRING**', request.httprequest.environ['QUERY_STRING'])
            # print (a)
            return self._create_order(**data)
        except Exception as e:
            return json.dumps({
            'code': 400,
            'code_error':str(e),
            'message': str(traceback.format_exc()),
            
        })

    def _create_order(self, **data):
        data_request =  request.httprequest.data
        data_request = data_request.decode("UTF-8")
        data_request = json.loads(data_request)
        # if not data_request.get('event').get('data').get('new'):
        #     return json.dumps({
        #         'code': 200,
        #         'message': 'Dữ liệu không tồn tại'
        #     })
        print ('***data***', data_request)
        payload = data_request['payload']
        event = payload['event']
        data = event['data']
        new = data['new']
        data = new
        # data = data_request.get('payload').get('event').get('data').get('new')
        original_so_id = data['id']
        print ('***original_so_id', original_so_id)
        order_info = data.get('order_info')
        user_info = data.get('user_info')
        phone = user_info.get('phone')
        user_id = user_info['user_id']
        if not phone:
            return json.dumps({
                'code': 200,
                'message': 'Phone không tồn tại'
            })
        else:
            phone = '0' + str(phone[3:])
       
        company_order_item_dict = {}

        for order_item in  order_info:
            company_id = order_item['company_id']
            company_order_item = company_order_item_dict.setdefault(company_id,[])
            company_order_item.append(order_item)
        sale_orders = []
        
        email = user_info['email']
        city = user_info['state']
        street = user_info['address']
        name = ''
        if user_info.get('first_name'):
            name = name + user_info.get('first_name')
        if user_info.get('last_name'):
            name = name + user_info.get('last_name')


        for company_id, company_order_items in company_order_item_dict.items(): 
            # partner = request.env['res.partner'].sudo().search([('phone', '=', phone), ('company_id', '=', company_id)], limit=1)
            partner = request.env['res.partner'].sudo().search([
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

            shipping_partner = request.env['res.partner'].sudo().search([
                ('parent_id', '=', partner.id), 
                ('company_id', '=', company_id), 
                ('street', '=', street),
                ('city', '=', city),
                ('type','=','delivery'),
                ('user_id','=',user_id)


            ], limit=1)

            if not shipping_partner:
                shipping_partner = request.env['res.partner'].sudo().create({
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
            } 
            
            sale_order = request.env['sale.order'].sudo().create(so_data)
            
            for item in company_order_items:
                so_line_data = {
                                        'product_id': item['id'],
                                        'product_uom_qty': float(item['qty']),
                                        'price_unit': float(item['price']),
                                        'discount': float(item['discount']),
                                        'order_id': sale_order.id,
                                    }
                sale_order_line = request.env['sale.order.line'].sudo().create(so_line_data)
    
            sale_orders.append(sale_order.id)
        # query = "update webshop.sale_orders set is_complete=true where id='%s'"%original_so_id
        # request.env.cr.execute(query)
        # rs = request.env.cr.fetchall()
        return json.dumps({
            'code': 200,
            'message': 'success',
            'sale_orders': sale_orders,
            'is_create_partner':is_create_partner,
            'is_shipping_partner_create':is_shipping_partner_create,
            # 'rs':rs
        })

