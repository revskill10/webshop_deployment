from odoo import models, fields, api
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    firebase_uid = fields.Char(string='Uid of firebase')




