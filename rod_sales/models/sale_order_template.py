from odoo import models, fields, api

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    user_id = fields.Many2one(
        'res.users',
        string='Vendedor',
        help='Vendedor asignado a esta plantilla de venta.',
        default=lambda self: self.env.user,
    )
