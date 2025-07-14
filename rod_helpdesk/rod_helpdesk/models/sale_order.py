
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket de Soporte')
