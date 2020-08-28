from odoo import models, fields, api
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
import base64

def get_attachment(self, field):
    domain = [
        ('res_model', '=', self._name),
        ('res_field', '=', field),
        ('res_id', '=', self.id),
    ]
    attachment = self.env['ir.attachment'].sudo().search(domain)
    return attachment   

def get_attachment_cloud_url(self, field):
    at = get_attachment(self, field)
    cloud_url = at.cloud_url
    return cloud_url


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    url_image_cloud_at = fields.Char(compute='_url_image_cloud_at', store=True)
    image = fields.Binary(upload=True)

    # def write(self, vals):
    #     return super(ProductTemplate, self.with_context(a=1)).write(vals)

    @api.depends('image')
    def _url_image_cloud_at(self):
        for r in self:
            r.url_image_cloud_at = \
            get_attachment_cloud_url(r, 'image')
        


    