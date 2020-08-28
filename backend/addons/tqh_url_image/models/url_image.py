from odoo import models, fields, api
from odoo.addons.tqh_url_image.models.product_template import _compute_url_image_view


class NdtProductImage(models.Model):
    _name = 'ndt.url.image'

    name = fields.Char()
    url_image = fields.Char(required=True)
    url_image_view = fields.Binary(compute='url_image_view_')
    product_category_id = fields.Many2one('product.category', ondelete='cascade')
    
    @api.depends('url_image')
    def url_image_view_(self):
        for r in self:
            r.url_image_view = _compute_url_image_view(r.url_image)