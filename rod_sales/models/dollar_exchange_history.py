from odoo import models, fields, api

class DollarExchangeHistory(models.Model):
    _name = 'dollar.exchange.history'
    _description = 'Dollar Exchange History'

    product_ids = fields.Many2one('product.product', string='Product')
    product_template_id = fields.Many2one('product.template', string='Product Template',ondelete='cascade')
    lot_name = fields.Char(string='Lote/N. Serie')
    date = fields.Date(string='Fecha', required=True)
    official_dollar_exchange = fields.Float(string='Dolar oficial', required=True)
    old_cost = fields.Float(string='Costo anterior', required=True)
    parallel_dollar_exchange = fields.Float(string='Dolar paralelo', required=True)
    new_cost = fields.Float(string='Costo actual', store=True)
