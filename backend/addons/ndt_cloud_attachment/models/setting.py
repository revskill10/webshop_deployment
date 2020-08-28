from odoo import models, fields, api, tools
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cloud_name = fields.Char() 
    api_key = fields.Char() 
    api_secret = fields.Char()
    # field_id = fields.Many2one('ir.model.fields')
    is_cloud_upload_attachment = fields.Boolean()

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            cloud_name=self.env['ir.config_parameter'].sudo().get_param('ndt_clound_image.cloud_name'),
            api_key=self.env['ir.config_parameter'].sudo().get_param('ndt_clound_image.api_key'),
            api_secret=self.env['ir.config_parameter'].sudo().get_param('ndt_clound_image.api_secret'),
            is_cloud_upload_attachment=self.env['ir.config_parameter'].sudo().get_param('ndt_clound_image.is_cloud_upload_attachment')
        )
        return res

    # @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().\
            set_param('ndt_clound_image.cloud_name', self.cloud_name)
        self.env['ir.config_parameter'].sudo().\
            set_param('ndt_clound_image.api_key', self.api_key)
        self.env['ir.config_parameter'].sudo().\
            set_param('ndt_clound_image.api_secret', self.api_secret)
        self.env['ir.config_parameter'].sudo().\
            set_param('ndt_clound_image.is_cloud_upload_attachment', self.is_cloud_upload_attachment)
        




