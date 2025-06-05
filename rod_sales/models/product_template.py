from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product template'

    profit_margin = fields.Float(string='Margen de ganancia %',
                                 digits=(12, 2),
                                 help="Porcentaje de ganancia que se aplicará al costo para calcular el precio de venta.")

    description = fields.Text(string='Descripción', translate=True)
    po_dollar_exchange_history = fields.One2many('dollar.exchange.history', 'product_template_id',
                                                 string='Historial de cambio de dólar', digits=(12, 2))

    @api.onchange('standard_price', 'profit_margin')
    def _onchange_standard_price_profit_margin(self):
        """
        Actualiza el precio de venta (list_price) cada vez que se modifique el costo (standard_price)
        o el porcentaje de profit_margin.
        """
        for record in self:
            # Si hay costo, se calcula el precio de venta
            if record.standard_price:
                record.list_price = record.standard_price * (1 + (record.profit_margin or 0.0) / 100.0)
            else:
                record.list_price = 0.0
    @api.model
    def default_get(self, fields_list):
        defaults = super(ProductTemplate, self).default_get(fields_list)
        if 'detailed_type' in fields_list:
            defaults['detailed_type'] = 'product'  # 'product' = almacenable
        return defaults

    def name_get(self):
        res = super().name_get()
        result = []
        for product_id, name in res:
            product = self.browse(product_id)
            name_with_stock = f"{name} - Disponible: {int(product.qty_available)}"
            result.append((product_id, name_with_stock))
        return result

    def _compute_display_name(self):
        for product in self:
            code = product.default_code or ""
            name = product.name or product.product_tmpl_id.name
            qty = int(product.qty_available)
            if code:
                product.display_name = f"[{code}] {name} - Disponible: [{qty}]"
            else:
                product.display_name = f"{name} - Disponible: [{qty}]"


