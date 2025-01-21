from odoo import models, fields, api

class AdditionalCosts(models.Model):
    _name = 'additional.costs'
    _description = 'Additional Costs'

    select_additional_costs = fields.Selection([
        ('supplier_invoice', 'Facturas de proveedores'),
        ('guarantee_slip', 'Boleta de garantia'),
        ('transportation_costs', 'Gastos de transporte'),
        ('legalized_documents', 'Documentos legalizados'),
        ('client_commission', 'Comision de cliente'),
    ], string='Costos adicionales', required=True)
    date = fields.Date(string='Fecha', required=True)
    amount = fields.Float(string='Monto', required=True, digits=(12, 2))
    sale_order_ids = fields.Many2one('sale.order', string='Productos')