from odoo import models, fields, api, tools
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError


class IrField(models.Model):
    _inherit = 'ir.model.fields'
    # is_upload_cloud = fields.Boolean()
