# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json

class Jsonb(fields.Char):
    column_cast_from = ('jsonb',)
    _slots = {
        'size': None,                   # maximum size of values (deprecated)
    }

    @property
    def column_type(self):
        return ('jsonb','jsonb')

    def convert_to_read(self, value, record, use_name_get=True):
        if isinstance(value,dict):
            value = str(value)
            value = value.replace("'",'"')
        return value
        
    def convert_to_column(self, value, record, values=None):
        if isinstance(value, dict):
            value = json.dumps(value)
        elif isinstance(value,str):
            value = value.replace("'",'"')
        return value

    def convert_to_cache(self, value, record, validate=True):
        if value and isinstance(value, str):
            value = value.replace("'",'"')
            value = json.loads(value)
        return value


class SOR(models.Model):
    _name = 'ndt.sor'

    order_info = Jsonb(default="{}")
    user_info = Jsonb(default="{}")
    user_id = fields.Integer()
    payment_url = fields.Char()# send
    payment_info = Jsonb(default="{}") # send
    payment_response = Jsonb(default="{}") # return url
    is_paid = fields.Boolean(default=False)
    delivery_info = Jsonb(default="{}")



    

    