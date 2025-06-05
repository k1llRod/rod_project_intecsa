from odoo import models, fields, api
from datetime import datetime, timedelta
from babel.dates import format_datetime
import pytz

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    readonly_user = fields.Boolean(string='Readonly User', compute='_compute_readonly_user')

    cost = fields.Float(string='Costo', store=True, compute='_compute_commission_total')
    cost_total = fields.Float(string='Costo total', store=True, compute='_compute_commission_total')
    commission_total = fields.Float(string='Comisión total', store=True, compute='_compute_commission_total')
    delivery_total = fields.Float(string='Gasto adicional dinamico', store=True, compute='_compute_commission_total')
    commission_percentage = fields.Float(string='Porcentaje de comisión', compute='_compute_commission_total')
    commission = fields.Float(string='Comision', store=True, compute='_compute_commission_total')
    margin_commission = fields.Monetary(string='Margen dinamico', store=True, compute='_compute_commission_total')

    validity_date = fields.Date(string='Fecha de validez', default=fields.Date.today())
    validity = fields.Selection([('5','5 dias'),('15','15 dias'),('30','30 dias')], string='Validez')
    validity_text = fields.Char(string='Validez')
    warranty = fields.Char(string='Garantía')
    delivery = fields.Date(string='Fecha entrega', default=fields.Date.today())
    delivery_text = fields.Char(string='Fecha de entrega')
    payment_method = fields.Selection([('transfer','Transferencia'),
                                       ('transfer_sigep', 'Transferencia SIGEP'),
                                       ('cheque','Cheque'),
                                       ('qr','QR')], string='Forma de pago')
    name_ent = fields.Char(string='Numero de Entrega')

    type_sale_id = fields.Many2one('type.sale', string='Tipo de venta')

    additional_costs_ids = fields.One2many('additional.costs', 'sale_order_ids', string='Costos adicionales')
    print_image = fields.Boolean(string='Imprimir imagen', default=False)

    state = fields.Selection(selection_add=[('approval', 'Aprobación')], ondelete={'approval': 'set default'})

    sale_order_template_id = fields.Many2one('sale.order.template', string='Plantilla de cotizacion', domain="[('user_id', '=', uid)]")

    date_order_text = fields.Char(string='Fecha de cotización', compute='_compute_date_order_text')

    @api.depends('date_order')
    def _compute_date_order_text(self):
        for record in self:
            tz = pytz.timezone('America/La_Paz')
            # Convertir la fecha a la zona horaria de La Paz
            record.date_order_text = format_datetime(record.date_order.astimezone(tz), "EEEE, d 'de' MMMM 'de' y", locale='es')

    def action_approve(self):
        """Método para aprobar la cotización y pasar a 'sale' (Pedido de Venta)"""
        for order in self:
            if order.state == 'draft':
                order.state = 'approval'

    def action_confirm(self):
        for order in self:
            if order.state != 'approval':
                # Lanza un error o pasa a 'approval' directamente, a tu elección
                # raise UserError("No puedes confirmar hasta que esté en aprobación")
                # order.state = 'approval'
                # return
                pass
        return super(SaleOrder, self).action_confirm()

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
            percentage = record.user_id.partner_id.commission_ids.percentage if record.user_id.partner_id.commission_ids.percentage else 0
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
            record.readonly_user = record.env.user.has_group("rod_sales.group_cost_readonly")


    def action_confirm(self):
        a = 1
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
                rec.price_unit = rec.env['stock.quant'].search([('product_id','=',rec.product_id.id)]).filtered(lambda x:x.location_id.usage == 'internal' or x.on_hand == True)[-1].price_unit
            if rec.product_id.tracking == 'serial' or rec.product_id.tracking == 'lot':
                for record in rec.lot_ids:
                    suma =  rec.env['stock.quant'].search([('lot_id','=',record.id)]).filtered(lambda x:x.quantity > 0).price_unit + suma
                    c += 1
                suma = round(suma / c, 2) if c > 0 else 0
                rec.price_unit = suma
                # rec.date_deadline = self.validity_date
                # rec.picking_id.scheduled_date = self.validity_date
        return res
    def _can_be_confirmed(self):
        self.ensure_one()
        return self.state in {'draft', 'sent', 'approval'}

    @api.onchange('type_sale_id')
    def _onchange_type_sale_id(self):
        for record in self:
            record.validity_date = fields.Date.today() + timedelta(days=record.type_sale_id.number_days)

    def sale_verification(self):
        pickings = self.env['stock.picking'].search([
            ('picking_type_code', '=', 'outgoing'),
            ('state', 'in', ['confirmed', 'assigned']),
            ('scheduled_date', '<', datetime.today()),
        ])
        # Cancelar los albaranes vencidos
        for picking in pickings:
            picking.do_unreserve()
            picking.action_cancel()

    def _create_invoices(self, grouped=False, final=False, date=None):
        """
        Sobreescribimos la creación de facturas para excluir productos con precio de venta 0
        y añadir apuntes contables adicionales configurados desde parámetros del sistema.
        """
        # 1. Llamar al método original para obtener las facturas
        invoices = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final, date=date)

        # 2. Filtrar las líneas con price_unit > 0
        for invoice in invoices:
            new_lines = invoice.invoice_line_ids.filtered(lambda line: line.price_unit > 0)
            invoice.write({'invoice_line_ids': [(6, 0, new_lines.ids)]})  # Reemplazar líneas
        # invoices.move_type = move_type  # Restaurar tipo de movimiento
        return invoices

    @api.model
    def cron_cancel_expired_quotations(self):
        """Cancela automáticamente las cotizaciones vencidas."""
        today = fields.Date.today()
        expired_orders = self.search([
            ('state', '=', 'draft'),  # Solo cotizaciones (no confirmadas)
            ('validity_date', '<', today)  # Que la fecha de vencimiento sea anterior a hoy
        ])

        for order in expired_orders:
            order.action_cancel()  # Cancela la cotización
            self.env.cr.commit()  # Guarda cambios para evitar bloqueos

    @api.model
    def create(self, vals):
        if 'warranty' in vals and vals.get('warranty'):
            vals['warranty'] = vals['warranty'].upper()
        if 'delivery_text' in vals and vals.get('delivery_text'):
            vals['delivery_text'] = vals['delivery_text'].upper()
        if 'validity_text' in vals and vals.get('validity_text'):
            vals['validity_text'] = vals['validity_text'].upper()
        return super(SaleOrder, self).create(vals)

    def write(self, vals):
        if 'warranty' in vals and vals.get('warranty'):
            vals['warranty'] = vals['warranty'].upper()
        if 'delivery_text' in vals and vals.get('delivery_text'):
            vals['delivery_text'] = vals['delivery_text'].upper()
        if 'validity_text' in vals and vals.get('validity_text'):
            vals['validity_text'] = vals['validity_text'].upper()
        return super(SaleOrder, self).write(vals)

    def update_cost(self):
        for record in self:
            picking = record.picking_ids.move_ids_without_package.stock_valuation_layer_ids
            for line in record.order_line:
                line.standard_price = picking.filtered(lambda x: x.product_id.id == line.product_id.id).unit_cost
        return True


