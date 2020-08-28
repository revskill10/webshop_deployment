# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BestSeller(models.Model):
    _name = 'ndt.bestseller'

    product_id = fields.Many2one('product.product')
    is_bestseller = fields.Boolean()
    is_bestview = fields.Boolean()
    is_new = fields.Boolean()
    sequence = fields.Integer()



    

    