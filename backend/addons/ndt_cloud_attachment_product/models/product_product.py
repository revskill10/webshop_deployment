from odoo import models, fields, api, tools
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from .product_template import get_attachment_cloud_url 
from odoo.addons.ndt_cloud_attachment.models.ir_attachment  import  cloud_url_read


class ProductProduct(models.Model):
    _inherit = 'product.product'

    url_image_cloud_at = fields.Char(
        "Url Image Cloud", compute='_url_image_cloud_at', store=True)

    url_image_cloud_variant_at = fields.Char(compute='_url_image_cloud_variant_at', store=True)

 
    @api.depends('image_variant')
    def _url_image_cloud_variant_at(self):
        for r in self:
            r.url_image_cloud_variant_at =\
                get_attachment_cloud_url(r, 'image_variant')
 
    @api.one
    @api.depends('url_image_cloud_variant_at', 'product_tmpl_id.url_image_cloud_at')
    def _url_image_cloud_at(self):
        self.url_image_cloud_at = self.url_image_cloud_variant_at
        if not self.url_image_cloud_at:
            self.url_image_cloud_at = self.product_tmpl_id.url_image_cloud_at

    @api.one
    @api.depends('url_image_cloud_at')
    def _compute_images(self):
        if not self.image:
            if self.env['ir.config_parameter'].sudo().get_param('ndt_clound_image.is_cloud_upload_attachment') and self.url_image_cloud_at:
                image = cloud_url_read(self.url_image_cloud_at)
                self.image_medium = image
                self.image_small = image
                self.image = image
            else:
                super()._compute_images()

        else:
            super()._compute_images()
