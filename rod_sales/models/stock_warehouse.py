from odoo import models, fields, api

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    street = fields.Char(string='Calle')
    street2 = fields.Char(string='Calle 2')
    city = fields.Char(string='Ciudad')
    state_id = fields.Many2one('res.country.state', string='Estado')
    zip = fields.Char(string='Código postal')
    country_id = fields.Many2one('res.country', string='País')
    phone = fields.Char(string='Teléfono')


