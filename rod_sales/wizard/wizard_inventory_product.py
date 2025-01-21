from odoo import models, fields, api
from odoo.exceptions import UserError

class WizardInventoryProduct(models.TransientModel):
    _name = 'wizard.inventory.product'
    _description = 'Wizard Inventory Product'

    # product_id = fields.Many2one('product.product', string='Producto')
    official_dollar_exchange = fields.Float(string='Cambio dolar oficial', readonly=True, default=lambda self: self._get_usd_rate(), digits=(12, 2))
    parallel_dollar_exchange = fields.Float(string='Cambio dolar paralelo', digits=(12, 2))
    product_ids  = fields.Many2many('product.product', string="Products with Stock", compute='get_products_with_stock')
    product_quants_id = fields.Many2many('stock.quant', string="Products with Stock", compute='get_products_with_stock')
    @api.model
    def _get_usd_rate(self):
        """
        Método para obtener la tasa de cambio del dólar automáticamente.
        """
        usd_currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        return 1.0 / usd_currency.rate if usd_currency and usd_currency.rate else 0.0

    @api.depends('official_dollar_exchange')
    def get_products_with_stock(self):
        """
        Obtiene todos los productos con cantidades a mano.
        """
        # quants = self.env['stock.quant'].search([('quantity', '>', 0)])
        quants = self.env['product.template'].search([('qty_available', '>', 0)]).product_variant_id
        product_quant = self.env['stock.quant'].search([('location_id.usage','=','internal'),("on_hand", "=", True),('product_id', 'in', quants.ids)])
        # product_ids = quants.mapped('product_id')
        self.product_quants_id = product_quant
        self.product_ids = quants

    def update_dollar_exchange(self):
        """
        Actualiza el cambio del dólar en los productos seleccionados.
        """
        if self.parallel_dollar_exchange <= 0:
            raise UserError('El cambio del dólar paralelo debe ser mayor a cero.')
        for product in self.product_quants_id:
            old_cost = round(product.price_unit, 2)
            old_change = round(old_cost / round(self.official_dollar_exchange,2),2)
            new_change = round(old_change * round(self.parallel_dollar_exchange, 2),2)
            product_update = product.write({
                'price_unit': new_change,
            })
            if product_update:
                self.env['dollar.exchange.history'].create({
                    'product_ids': product.product_id.id,
                    'lot_name': product.lot_id.name,
                    'date': fields.Date.today(),
                    'official_dollar_exchange': self.official_dollar_exchange,
                    'old_cost': old_cost,
                    'parallel_dollar_exchange': self.parallel_dollar_exchange,
                    'new_cost': new_change,
                })
        for prod in self.product_ids:
            total = sum(prod.stock_quant_ids.filtered(lambda x:x.location_id.usage == 'internal').mapped('price_unit'))
            quantity = len(prod.stock_quant_ids.filtered(lambda x:x.location_id.usage == 'internal'))
            total_val = total / quantity
            prod.list_price = (total_val * (prod.profit_margin / 100)) + total_val
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }