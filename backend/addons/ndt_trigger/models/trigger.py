# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Trigger(models.TransientModel):
    _name = 'ndt_trigger.trigger'
    _description = 'Trigger'

    offset = fields.Integer()
    limit = fields.Integer()
    count = fields.Integer()
    trigger_value = fields.Boolean(default=True)
    model_id = fields.Many2one('ir.model')
    function = fields.Char()


    # def search_method(self):
    #     args = [[]]
    #     kwargs = {}
    #     if self. limit:
    #         kwargs = {'limit':self. limit}
    #     if self.offset:
    #         kwargs = {'offset':self. offset}
    #     return args, kwargs

    # @api.multi
    def run_function(self):
        objects = self.env[self.model_id.model].search([], offset=self.offset, limit=self.limit)
        function =  getattr(objects, self.function)
        function()
        self.count = len(objects)
        self.offset = self.offset +  self.count


    # @api.multi
    def run_function_by_id_for_cronjob(self, id):
        obj = self.browse(id)
        obj.run_function()
        
        
    
       
    

    