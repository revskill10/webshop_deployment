# -*- coding: utf-8 -*-
from odoo import models, fields, api
from unidecode import unidecode
import re


def _compute_slug(name, id):
    name = unidecode(name)
    name = re.sub('\s+','-',name)
    name = re.sub('\W','-',name, flags=re.I)
    name = re.sub('-{2,}','-', name)
    name = name.lower()
    name  = name + '_' + str(id)
    return name

class ProductBrand(models.Model):
    _inherit = 'product.brand'

    url_image = fields.Char()
    slug = fields.Char(compute='_compute_slug', store=True)

    @api.depends('name')
    def _compute_slug(self):
        for r in self:
            if r.name and r.id:
                r.slug =  _compute_slug(r.name, r.id)

    
    