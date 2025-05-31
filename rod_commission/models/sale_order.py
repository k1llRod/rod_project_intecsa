from odoo import models, fields, api, _
from datetime import datetime

class SaleOrder(models.Model):
    _inherit ='sale.order'

    payment_comision = fields.Boolean(string='Pago de comisión', default=False)
    payment_comision_id = fields.Many2one('seller.commission', string='Pago de comisión')
    date_invoice = fields.Date(string='Fecha de factura', related='invoice_ids.invoice_date')
    def action_create_payment(self):
        for rec in self:
            rec.payment_comision = True
            supplier = sum(line.amount for line in rec.additional_costs_ids if line.select_additional_costs == 'supplier_invoice')
            guarantee = sum(line.amount for line in rec.additional_costs_ids if line.select_additional_costs == 'guarantee_slip')
            transportation = sum(line.amount for line in rec.additional_costs_ids if line.select_additional_costs == 'transportation_costs')
            legalized = sum(line.amount for line in rec.additional_costs_ids if line.select_additional_costs == 'legalized_documents')
            client = sum(line.amount for line in rec.additional_costs_ids if line.select_additional_costs == 'client_commission')
            cost = sum(line.standard_price * line.product_uom_qty for line in rec.order_line)
            create_payment = self.env['seller.commission'].create({
                'agent_id': rec.user_id.id,
                'sale_id': rec.id,
                'amount_untaxed': rec.amount_untaxed,
                'amount_tax': rec.amount_tax,
                'amount_total': rec.amount_total,
                # 'cost_total': rec.cost_total,
                'cost_total': cost,
                'total': rec.commission_total,
                'date_from': datetime.today(),
                'supplier_invoice': supplier,
                'guarantee_slip': guarantee,
                'transportation_costs': transportation,
                'legalized_documents': legalized,
                'client_commission': client,
                'state': 'draft',
            })
            rec.payment_comision_id = create_payment.id