# models/helpdesk_ticket.py
from odoo import models, fields
from odoo.exceptions import UserError

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    accessory_line_ids = fields.One2many('helpdesk.ticket.accessory.line', 'ticket_id', string='Accesorios entregados')
    marca = fields.Char(string='Marca', help="Marca del producto o accesorio entregado")
    modelo = fields.Char(string='Modelo', help="Modelo del producto o accesorio entregado")
    serial_number = fields.Char(string='Numero serie', help="Número de serie del producto o accesorio entregado")
    sale_order_id = fields.One2many('sale.order', 'ticket_id', string='Ventas')
    sale_order_count = fields.Integer(
        compute="_compute_sale_order_count",
        string="Nº de pedidos"
    )

    def _compute_sale_order_count(self):
        for ticket in self:
            ticket.sale_order_count = len(ticket.sale_order_id)
    def action_view_sale_orders(self):
        self.ensure_one()
        action = self.env.ref("sale.action_quotations_with_onboarding").read()[0]
        action["domain"] = [("id", "in", self.sale_order_id.ids)]
        return action
    def create_sale_orders(self):
        for ticket in self:
            if not ticket.partner_id:
                raise UserError("Debe asignar un cliente al ticket antes de crear una venta.")

            sale = self.env['sale.order'].create({
                'partner_id': ticket.partner_id.id,
                'origin': ticket.name,
                'client_order_ref': ticket.description or ticket.name,
                'ticket_id': ticket.id if 'ticket_id' in self.env['sale.order']._fields else False,
            })
            # ticket.sale_order_id = sale.id
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'res_id': sale.id,
                'view_mode': 'form',
                'target': 'current',
            }
