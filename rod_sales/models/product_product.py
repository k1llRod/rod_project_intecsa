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