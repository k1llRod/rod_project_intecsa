from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    po_dollar_exchange_history = fields.One2many('dollar.exchange.history', 'product_ids', string='Historial de cambio de dólar')