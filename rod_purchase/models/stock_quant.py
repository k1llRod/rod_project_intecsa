from odoo import models, fields, api

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    price_unit = fields.Float(string='Precio unidad',store=True)
    price = fields.Float(string='Precio',compute='_compute_price',store=True)

    def _compute_price(self):
        for record in self:
            record.price = record.standard_price * record.quantity

    # @api.model
    # def create(self, vals):
    #     res = super(StockQuant, self).create(vals)
    #     picking = 0
    #     if res.product_id.tracking == 'none':
    #         picking= res.product_id.standard_price
    #     if res.product_id.tracking == 'serial':
    #         picking = self.env['stock.move.line'].search([('lot_id', '=', res.lot_id.name)]).picking_id.move_ids_without_package.filtered(lambda x:x.product_id.id == vals['product_id'])[-1].price_unit
    #     if res.product_id.tracking == 'lot':
    #         # picking = self.env['stock.move.line'].search([('name', '=', res.lot_id.name)]).picking_id
    #         picking = self.env['stock.move.line'].search([('lot_id', '=', res.lot_id.name)]).picking_id.move_ids_without_package.filtered(lambda x:x.product_id.id == vals['product_id'])[-1].price_unit
    #     res.price_unit = picking
    #     return res