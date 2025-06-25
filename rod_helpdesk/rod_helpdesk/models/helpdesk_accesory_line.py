# models/helpdesk_accessory_line.py
from odoo import models, fields

class HelpdeskTicketAccessoryLine(models.Model):
    _name = 'helpdesk.ticket.accessory.line'
    _description = 'Accesorios entregados en el ticket de soporte'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket')
    # product_id = fields.Many2one('product.product', string='Producto/Accesorio', required=True)
    accesory_description = fields.Char(string='Accesorio', required=True)
    quantity = fields.Float(string='Cantidad', default=1.0)
    notes = fields.Char(string='Observaciones')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Entregado'),
        ('devolution', 'Devuelto'),
    ], string='Estado', default='draft', required=True)
