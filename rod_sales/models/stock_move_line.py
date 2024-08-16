from odoo import models, fields, api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    price_unit_sale = fields.Float(string='Precio unidad venta', compute='_price_unit_sale',store=True)

    @api.depends('product_id')
    def _price_unit_sale(self):
        for record in self:
            record.price_unit_sale = record.product_id.lst_price
