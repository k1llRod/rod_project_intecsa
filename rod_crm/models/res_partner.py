from odoo import models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            args = args + ['|','|' ,('name', operator, name), ('email', operator, name), ('complete_name', operator, name)]
        return self.search(args, limit=limit).name_get()