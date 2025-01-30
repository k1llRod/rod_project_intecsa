from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product template'

    profit_margin = fields.Float(string='Margen de ganancia %', digits=(12, 2))
    description = fields.Text(string='Descripción', translate=True)
    po_dollar_exchange_history = fields.One2many('dollar.exchange.history', 'product_ids',
                                                 string='Historial de cambio de dólar', digits=(12, 2))
    # date = fields.Date(string='Date', required=True)
    # official_dollar_exchange = fields.Float(string='Official Dollar Exchange', required=True, digits=(12, 2))
    # old_cost = fields.Float(string='Old Cost', required=True, digits=(12, 2))
    # parallel_dollar_exchange = fields.Float(string='Parallel Dollar Exchange', required=True, digits=(12, 2))
    # new_cost = fields.Float(string='Costo', store=True, digits=(12, 2))



