from odoo import models, fields, api, tools
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
import multiprocessing
# from .product_template import upload_to_cloud_from_id 
import os
import base64
import logging
_logger = logging.getLogger(__name__)

from urllib import request
import cloudinary
import cloudinary.uploader
import cloudinary.api
from odoo.tools.mimetypes import guess_mimetype

st_IS_STORE_FILE = True

headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' }
def request_html(url, try_again=1, is_decode_utf8 = True, headers=headers):
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

def cloud_url_read(cloud_url):
    html_photo = request_html(cloud_url, False, is_decode_utf8 = False)
    if html_photo:
        photo = base64.encodestring(html_photo)
    else:
        photo = False
    return photo

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    cloud_url = fields.Char()
    
    # @api.one
    def _cloud_url_read(self, cloud_url):
        html_photo = request_html(cloud_url, False, is_decode_utf8 = False)
        if html_photo:
            photo = base64.encodestring(html_photo)
        else:
            photo = False
        return photo 

    @api.depends('store_fname', 'db_datas')
    def _compute_datas(self):
        bin_size = self._context.get('bin_size')
        for attach in self:
            datas = False
            if self.env['ir.config_parameter'].sudo().get_param('ndt_clound_image.is_cloud_upload_attachment') and attach.cloud_url:
                datas = self._cloud_url_read(attach.cloud_url)
                attach.datas = datas
            else:
                if attach.store_fname:
                    attach.datas = self._file_read(attach.store_fname, bin_size)
                else:
                    attach.datas = attach.db_datas

    def upload_image(self, value):
        mimetype = guess_mimetype(base64.b64decode(value))
        cloud_url = False
        if not 'image' in mimetype:
            return cloud_url
        cloudinary.config( 
        cloud_name = "phanmemqlhs", 
        api_key = "681918874796123", 
        api_secret = "9XXvTpVNH8ADgcw3T7XfXRfWsxE" 
        )
        encoded_string = value
        encoded_string = encoded_string.decode('utf-8')
        try:
            encoded_string ='data:%s;base64,'%mimetype + encoded_string
            
            rs = cloudinary.uploader.upload(encoded_string)
            cloud_url =  rs['url']
            print ('***tra ve cloud_url', cloud_url)
        except:
            pass
        return cloud_url

    def _inverse_datas(self):
        location = self._storage()
        for attach in self:
            # compute the fields that depend on datas
            value = attach.datas
            bin_data = base64.b64decode(value) if value else b''
            vals = {
                'file_size': len(bin_data),
                'checksum': self._compute_checksum(bin_data),
                'index_content': self._index(bin_data, attach.datas_fname, attach.mimetype),
                'store_fname': False,
                'db_datas': value,
            }
            cloud_url= False
            if self.env['ir.config_parameter'].sudo().get_param('ndt_clound_image.is_cloud_upload_attachment'):
                cloud_url = self.upload_image(value)
            vals['cloud_url'] = cloud_url
            if value and location != 'db':
                # save it to the filestore
                if st_IS_STORE_FILE:
                    store_fname = self._file_write(value, vals['checksum'])
                else:
                    store_fname = False
                vals['store_fname'] = store_fname
                vals['db_datas'] = False
            
            # take current location in filestore to possibly garbage-collect it
            fname = attach.store_fname
            # write as superuser, as user probably does not have write access
            super(IrAttachment, attach.sudo()).write(vals)
            if fname:
                self._file_delete(fname)
    

