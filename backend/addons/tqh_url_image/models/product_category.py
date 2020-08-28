from odoo import models, fields, api
# from odoo.addons.tqh_url_image.models.product_template import _compute_url_image_view


# class NdtProductImage(models.Model):
#     _name = 'ndt.url.image'

#     url_image = fields.Char(required=True)
#     url_image_view = fields.Binary(compute='url_image_view_')
#     product_category_id = fields.Many2one('product.category', ondelete='cascade')
    
#     @api.depends('url_image')
#     def url_image_view_(self):
#         for r in self:
#             r.url_image_view = _compute_url_image_view(r.url_image)

class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    
    is_web_publish = fields.Boolean()
    url_image = fields.Char()
    url_image_ids = fields.One2many('ndt.url.image', 'product_category_id')
    url_images = fields.Char(compute='_compute_url_images', store=True)
    short_desc = fields.Char()
    is_banner = fields.Boolean()

    @api.depends('url_image_ids')
    def _compute_url_images(self):
        for r in self:
            r.url_images = ','.join(r.url_image_ids.mapped('url_image'))