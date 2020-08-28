from odoo import models, fields, api, tools
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from .product_template import _compute_url_image_view
class ProductTemplate(models.Model):
    _inherit = 'product.product'
    
    url_image = fields.Char(
        "Url Image", compute='_compute_url_images', inverse='_set_url_image', store=True)
    url_image_variant = fields.Char()
    image_stiker_id = fields.Many2one('ndt.url.image', string='Ảnh khuyến mãi')
    image_stiker_id_view = fields.Binary(related='image_stiker_id.url_image_view',string='Ảnh khuyến mãi view')
 
    @api.one
    def _set_url_image(self):
        if self.product_tmpl_id.url_image and self.product_variant_count > 1:
            self.url_image_variant = self.url_image
        else:
            self.url_image_variant = False
            self.product_tmpl_id.url_image = self.url_image

    @api.one
    @api.depends('url_image_variant', 'product_tmpl_id.url_image')
    def _compute_url_images(self):
        self.url_image = self.url_image_variant
        if not self.url_image:
            self.url_image = self.product_tmpl_id.url_image


    # @api.one
    # @api.depends('url_image')
    # def _compute_images(self):
    #     if not self.image:
    #         if self.url_image:
    #             image = _compute_url_image_view(self.url_image)
    #             self.image_medium = image
    #             self.image_small = image
    #             self.image = image
    #         else:
    #             super()._compute_images()



    # @api.one
    # @api.depends('image_variant', 'product_tmpl_id.image')
    # def _compute_images(self):
    #     if self._context.get('bin_size'):
    #         self.image_medium = self.image_variant or self.url_image_view
    #         self.image_small = self.image_variant or self.url_image_view
    #         self.image = self.image_variant or self.url_image_view
    #     else:
    #         resized_images = tools.image_get_resized_images(self.image_variant or self.url_image_view, return_big=True, avoid_resize_medium=True)
    #         self.image_medium = resized_images['image_medium']
    #         self.image_small = resized_images['image_small']
    #         self.image = resized_images['image']
    #     if not self.image_medium:
    #         self.image_medium = self.product_tmpl_id.image_medium
    #     if not self.image_small:
    #         self.image_small = self.product_tmpl_id.image_small
    #     if not self.image:
    #         self.image = self.product_tmpl_id.image




