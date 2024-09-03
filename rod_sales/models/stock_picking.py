from odoo import models, fields, api

class StockPickin(models.Model):
    _inherit = 'stock.picking'
    name_ent = fields.Char(string="Numero de entrega")
    def button_validate(self):
        res = super(StockPickin, self).button_validate()
        if self.picking_type_id.code == 'outgoing':
            for line in self.move_ids_without_package:
                line.sale_line_id.purchase_price = line.price_unit
                line.sale_line_id.standard_price = line.price_unit
        sequence = self.env['ir.sequence'].next_by_code('stock.picking')
        self.name_ent  = sequence
        self.sale_id.name_ent = sequence
        return res