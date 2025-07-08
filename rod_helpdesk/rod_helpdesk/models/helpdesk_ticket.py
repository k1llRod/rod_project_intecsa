# models/helpdesk_ticket.py
from odoo import models, fields

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    accessory_line_ids = fields.One2many('helpdesk.ticket.accessory.line', 'ticket_id', string='Accesorios entregados')
    marca = fields.Char(string='Marca', help="Marca del producto o accesorio entregado")
    modelo = fields.Char(string='Modelo', help="Modelo del producto o accesorio entregado")
    serial_number = fields.Char(string='Numero serie', help="Número de serie del producto o accesorio entregado")