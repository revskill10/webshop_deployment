from odoo import models, fields, api
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
import base64
from time import sleep
from urllib import request
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' }
def request_html(url, try_again=1, is_decode_utf8 = True, headers=headers):
    # count_fail = 0
    def in_try():
        req =request.Request(url, None, headers)
        rp= request.urlopen(req)
        mybytes = rp.read()
        if is_decode_utf8:
            html = mybytes.decode("utf8")
            return html
        else:
            return mybytes
    try:
        html = in_try()
    except:
        html = False
    return html
def _compute_url_image_view(url_image):
    if url_image:
        
        html_photo = request_html(url_image, False, is_decode_utf8 = False)
        if html_photo:
            photo = base64.encodestring(html_photo)
        else:
            photo = False
        return photo 
def cloud_url_read(cloud_url):
    html_photo = request_html(cloud_url, False, is_decode_utf8 = False)
    if html_photo:
        photo = base64.encodestring(html_photo)
    else:
        photo = False
    return photo
    
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    url_image = fields.Char()
    url_image_view = fields.Binary(compute='url_image_view_')

    @api.depends('url_image')
    def url_image_view_(self):
        for r in self:
            r.url_image_view = _compute_url_image_view(r.url_image)
     