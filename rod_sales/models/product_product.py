from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    po_dollar_exchange_history = fields.One2many('dollar.exchange.history', 'product_ids', string='Historial de cambio de dólar')

    @api.model
    def create(self, vals):
        # Si no se especifica default_code en la creación, se asigna el correlativo generado
        if not vals.get('default_code'):
            seq = self.env['ir.sequence'].next_by_code('product.product.sequence')
            if seq:
                vals['default_code'] = seq
        return super(ProductProduct, self).create(vals)

    # @api.depends('name', 'default_code', 'qty_available')
    # def _compute_display_name(self):
    #     super()._compute_display_name()  # Llamamos primero al original
    #
    #     for product in self:
    #         # Añadimos al final del nombre la cantidad disponible
    #         product.display_name = f"{product.display_name} - Disponible: {int(product.qty_available)}"
    # @api.depends('name', 'default_code', 'qty_available')
    # def _compute_display_name(self):
    #     for product in self:
    #         qty = int(product.qty_available)
    #         product.product_template_id.name = f"[{product.name}] - Disponible: [{qty}]"