# -*- coding: utf-8 -*-
from odoo import models, fields, api
from unidecode import unidecode
import re

def _compute_seo_url(name, r_id):
    name = unidecode(name)
    name = re.sub('\s+','-',name)
    # name = re.sub(',|\(|\)','',name, flags=re.I)
    name +='-' + str(r_id)
    name = re.sub('\W','-',name, flags=re.I)
    name = re.sub('-{2,}','-', name)
    name = name.lower()
    return name

class Product(models.Model):
    _inherit = 'product.product'

    seo_url = fields.Char(compute='_compute_seo_url', store=True)

    @api.depends('product_tmpl_id.name','attribute_value_ids')
    def _compute_seo_url(self):
        for r in self:
            if r.id:
                name = r.name_get()[0][1]
                r_id = r.id
                name = _compute_seo_url(name, r_id)
                r.seo_url = name


    