# -*- coding: utf-8 -*-
from json import dumps
import json
from odoo import http
from odoo.http import request, Response
import traceback
import logging
_logger = logging.getLogger(__name__)





class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)

class ResPartnerAPI(http.Controller):

    @http.route('/api/ndt/delevery_get_price', type='json', auth='none', methods=['POST'], csrf=False)
    def change_password_admin(self, **data):
        data_request =  request.httprequest.data
        data_request = data_request.decode("UTF-8")
        data_request = json.loads(data_request)
        
        carrier_id = data_request['carrier_id']
        order = data_request['order']
        order = obj(order)
        # password = data_request['password']
        
        # order = request.env['sale.order'].browse(52).sudo()
        # order = request.env['sale.order']
        # order.company_id = request.env['res.company'].browse(1)
        carrier = request.env['delivery.carrier'].browse(carrier_id).sudo()
        # order = {"carrier_id":2,
# "order":{
#     "amount_total":100,
#     "partner_shipping_id":false,
#     "state":"draft",
#     "order_line":[{"product_id":1,"weight":10,"volumn":false, "qty":5}],
#     "is_delivery":false

# }
# }
        # order = obj(order)
        rs = carrier.base_on_rule_rate_shipment2(order)
        rt = {
            'code': 200,
            'message': 'OK',
        }
        rt.update(rs)
        return json.dumps(rt)

   