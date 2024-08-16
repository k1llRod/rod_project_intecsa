from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    standard_price = fields.Float(string='Costo')
    delivery_cost = fields.Float(string='Costo de envío')

    @api.onchange('product_template_id')
    def _onchange_product_id(self):
        for record in self:
            if record.product_template_id.tracking == 'serial':
                record.standard_price = record.product_template_id.standard_price

    @api.model
    def create(self, vals):
        # Crear la línea de producto original
        if self.env['sale.order'].search([('id','=',vals['order_id'])]).order_line.filtered(lambda x:x.name == vals['name'] and x.display_type == 'line_note'):
            sw = True
            vals = []
        else:
            sw = False
        # vals = [] if vals['display_type'] == 'line_note' else vals
        order_line = super(SaleOrderLine, self).create(vals)
        # Crear la línea de nota automáticamente
        if order_line.product_id.description:
            note_vals = {
                'order_id': order_line.order_id.id,
                'product_id': False,
                'display_type': 'line_note',
                'name': order_line.product_id.description if order_line.product_id.description else 'Note for the product line',
                'sequence': order_line.sequence + 1,
                # Esto asegura que la nota aparezca después de la línea del producto
            }
            super(SaleOrderLine, self).create(note_vals)

        return order_line
