from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        picking = self.picking_ids
        for pick in picking:
            for line in pick.move_ids_without_package:
                line.price_unit = round(line.purchase_line_id.price_subtotal / line.product_qty, 2)
        return res

    @api.model
    def create(self, vals):
        user_warehouse = self.env.user.property_warehouse_id
        if user_warehouse:
            vals['picking_type_id'] = user_warehouse.in_type_id.id
        return super(PurchaseOrder, self).create(vals)