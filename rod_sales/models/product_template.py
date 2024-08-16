from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product template'

    description = fields.Text(string='Descripción', translate=True)


