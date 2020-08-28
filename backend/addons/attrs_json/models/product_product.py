# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
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

class Product(models.Model):
    _inherit = 'product.product'
    pcateg_id = fields.Many2one(related='categ_id', store=True)
    pname = fields.Char(related='name', store=True)
    lst_price = fields.Float(
        'Sale Price', compute='_compute_product_lst_price', store=True,
        digits=dp.get_precision('Product Price'), inverse='_set_product_lst_price',
        help="The sale price is managed from the product template. Click on the 'Configure Variants' button to set the extra attribute prices.")
    pproduct_brand_id = fields.Many2one(related='product_brand_id', store=True)
    attrs_jsonb = Jsonb(compute='attrs_jsonb_', store=True)
    # a = fields.Binary(attachment=False)
    # attrs_json1 = Jsonb()

    @api.depends('attribute_value_ids')
    def attrs_jsonb_(self):
        for r in self:
            adict = {}
            for attr in r.attribute_value_ids:
                attribute_id = str(attr.attribute_id.id)
                adict[attribute_id] = attr.id
            r.attrs_jsonb = adict


    def attrs_jsonb_cronjob(self):
        rs = self.search([],limit=100)
        for r in rs:
            r.attrs_jsonb_()

    #select * from product_product where attrs_jsonb @> '{"size":3}'::jsonb
    # attrs_json = fields.Json()

    # def _attrs_jsonb_show(self):
    #     for r in self:
    #         query = '''SELECT attrs_jsonb from product_product
    #         WHERE id = %s'''%(r.id)
    #         self.env.cr.execute(query)
    #         rs = self.env.cr.dictfetchall()
    #         if rs:
    #             rs = rs[0]['attrs_jsonb']
    #             r. attrs_jsonb_show = rs

    # def update_attrs_jsonb(self,obj, vals):
    #     if 'attribute_value_ids' in vals:
    #         for r in obj:
    #             adict = {}
    #             for attr in r.attribute_value_ids:
    #                 attribute_id = attr.attribute_id.name
    #                 adict[attribute_id] = attr.id
    #                 query = '''UPDATE product_product
    #                 SET attrs_jsonb = '%s'::jsonb
    #                 WHERE id = %s'''%(json.dumps(adict), r.id)
    #                 self.env.cr.execute(query)


    # @api.model
    # def create(self,vals):
    #     rs = super(Product, self.sudo()).create(vals)
    #     self.update_attrs_jsonb(rs, vals)
    #     return rs

   
    # @api.multi
    # def write(self, vals):
    #     rs = super(Product, self.sudo()).write(vals)
    #     self.update_attrs_jsonb(self, vals)
    #     return rs