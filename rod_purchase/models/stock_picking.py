from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        picking_id = self.id
        if self.picking_type_id.code == 'incoming':
            for line in self.move_ids_without_package:
                if line.product_id.tracking == 'none':
                    for quant in self.env['stock.quant'].search([('product_id','=',line.product_id.id)]):
                        if quant.quantity > 0:
                            quant.price_unit = line.price_unit
                    # line.price_unit = line.move_line_ids.move_id.price_unit
                if line.product_id.tracking == 'serial' or line.product_id.tracking == 'lot':
                    for quant in line.lot_ids.quant_ids:
                        if quant.quantity > 0:
                            quant.price_unit = line.price_unit
        return res