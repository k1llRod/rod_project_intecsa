from odoo import models, fields, api
from datetime import datetime, timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    readonly_user = fields.Boolean(string='Readonly User', store=True, compute='_compute_readonly_user')

    cost = fields.Float(string='Costo', store=True, compute='_compute_commission_total')
    cost_total = fields.Float(string='Costo total', store=True, compute='_compute_commission_total')
    commission_total = fields.Float(string='Comisión total', store=True, compute='_compute_commission_total')
    delivery_total = fields.Float(string='Gasto adicional dinamico', store=True, compute='_compute_commission_total')
    commission_percentage = fields.Float(string='Porcentaje de comisión', compute='_compute_commission_total')
    commission = fields.Float(string='Comision', store=True, compute='_compute_commission_total')
    margin_commission = fields.Monetary(string='Margen dinamico', store=True, compute='_compute_commission_total')

    validity = fields.Char(string='Validez')
    warranty = fields.Char(string='Garantía')
    delivery = fields.Char(string='Entrega')
    payment_method = fields.Selection([('transfer','Transferencia'),('cheque','Cheque'),('qr','QR')], string='Forma de pago')
    name_ent = fields.Char(string='Numero de Entrega')

    type_sale_id = fields.Many2one('type.sale', string='Tipo de venta')

    additional_costs_ids = fields.One2many('additional.costs', 'sale_order_ids', string='Costos adicionales')
    def _compute_commission_percentage(self):
        for record in self:
            record.commission_percentage = 10
    @api.depends('order_line', 'additional_costs_ids')
    def _compute_cost_total(self):
        for record in self:
            # record.delivery_total = sum(line.delivery_cost for line in record.order_line)
            record.delivery_total = sum(line.amount for line in record.additional_costs_ids)
            record.cost_total = sum(line.standard_price * line.product_uom_qty for line in record.order_line) + record.delivery_total
            record.margin_commission = record.amount_untaxed - record.cost_total
    # @api.depends('select_additional_costs')
    # def _compute_additional_costs(self):
    #     for record in self:
    #         record.delivery_total = sum(line.amount for line in record.additional_costs_ids)

    @api.depends('order_line', 'additional_costs_ids')
    def _compute_commission_total(self):
        for record in self:
            percentage = self.env.user.partner_id.commission_ids.percentage if self.env.user.partner_id.commission_ids else 0
            record.commission_percentage = percentage/100 if percentage else 0
            record.delivery_total = sum(line.amount for line in record.additional_costs_ids)
            record.cost_total = sum(line.standard_price * line.product_uom_qty for line in record.order_line) + record.delivery_total
            record.margin_commission = record.amount_untaxed - record.cost_total
            record.commission_total = record.margin_commission * (percentage/100)
            record.readonly_user = record.create_uid.has_group("rod_sales.group_cost_readonly")

            # record.commission_total = record.commission
    @api.depends('partner_id', 'create_uid')
    def _compute_readonly_user(self):
        for record in self:
            record.readonly_user = record.create_uid.has_group("rod_sales.group_cost_readonly")


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        picking = self.picking_ids[-1].move_ids_without_package
        for record in self.picking_ids:
            if record.state == 'confirmed' or record.state == 'borrador':
                record.scheduled_date = self.validity_date
        suma = 0
        for rec in picking:
            c = 0
            suma = 0
            if rec.product_id.tracking == 'none':
                rec.price_unit = rec.product_id.standard_price
            if rec.product_id.tracking == 'serial' or rec.product_id.tracking == 'lot':
                for record in rec.lot_ids:
                    suma =  self.env['stock.quant'].search([('lot_id','=',record.id)]).filtered(lambda x:x.quantity > 0).price_unit + suma
                    c += 1
                suma = round(suma / c, 2) if c > 0 else 0
                rec.price_unit = suma
                # rec.date_deadline = self.validity_date
                # rec.picking_id.scheduled_date = self.validity_date
        return res

    @api.onchange('type_sale_id')
    def _onchange_type_sale_id(self):
        for record in self:
            record.validity_date = fields.Date.today() + timedelta(days=record.type_sale_id.number_days)

    def sale_verification(self):
        pickings = self.env['stock.picking'].search([('state', '=', 'confirmed'),('scheduled_date', '<', datetime.today())])
        # Cancelar los albaranes vencidos
        for picking in pickings:
            picking.action_cancel()