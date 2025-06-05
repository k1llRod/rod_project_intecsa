from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for rec in self:
            if rec.move_type == 'out_invoice':
                sale_id = self.env['sale.order'].search([('name', '=', rec.invoice_origin)], limit=1)
                if sale_id:
                    # rec.payment_comision = True
                    create_payment = self.env['seller.commission'].create({
                        'agent_id': rec.user_id.id,
                        'sale_id': sale_id.id,
                        'amount_untaxed': sale_id.amount_untaxed,
                        'amount_tax': sale_id.amount_tax,
                        'amount_total': sale_id.amount_total,
                        'cost_total': sale_id.cost_total,
                        'delivery_total': sale_id.delivery_total,
                        'total': sale_id.commission_total,
                        'date_from': datetime.today(),
                        'state': 'draft',
                    })
        return res

    # def action_create_invoice(self):
    #     res = super().action_create_invoice()
    #     for order in self:
    #         invoices = order.invoice_ids.filtered(lambda inv: inv.state in ['draft', 'posted'])
    #         for invoice in invoices:
    #             invoice.invoice_line_ids.create({
    #                 'invoice_id': invoice.id,
    #                 'name': 'Gasto adicional',
    #                 'quantity': 1,
    #                 'price_unit': 100.00,  # cambia esto por el monto del gasto
    #                 'account_id': self.env['account.account'].search([('code', '=', '610101')], limit=1).id,
    #                 # busca una cuenta válida
    #                 'product_id': self.env.ref('product.product_product_consultant').id,  # opcional, puedes omitirlo
    #             })
    #     return res
    # def action_register_payment(self):
    #     for move in self:
    #         if move.move_type == 'out_invoice':
    #             sale_orders = move.invoice_line_ids.mapped('sale_line_ids.order_id')
    #             if sale_orders:
    #                 sale_order = sale_orders[0]  # Tomamos el primero
    #                 if not sale_order.payment_comision_id:
    #                     sale_order.action_create_payment()
    #                 # Crear asiento de gastos si no existe
    #                 # if not sale_order.expense_move_id:
    #                 #     sale_order.create_account_move_expenses(move)
    #     return super().action_register_payment()

    def action_create_payments(self):
        res = super().action_create_payments()

        for move in self:
            # Validamos que sea una factura cliente y esté posteada
            if move.move_type == 'out_invoice' and move.state == 'posted':
                # Solo ejecutar si el pago realmente se realizó (verificamos si tiene líneas reconciliadas)
                if any(line.reconciled for line in move.line_ids if line.account_id.internal_type == 'receivable'):
                    # Buscar la orden de venta asociada
                    sale_order = self.env['sale.order'].search([('invoice_ids', 'in', move.ids)], limit=1)
                    if sale_order and not sale_order.payment_comision:
                        # Crear comisión si corresponde
                        cost = sum(line.standard_price * line.product_uom_qty for line in sale_order.order_line)
                        supplier = sum(line.amount for line in sale_order.additional_costs_ids if
                                       line.select_additional_costs == 'supplier_invoice')
                        guarantee = sum(line.amount for line in sale_order.additional_costs_ids if
                                        line.select_additional_costs == 'guarantee_slip')
                        transportation = sum(line.amount for line in sale_order.additional_costs_ids if
                                             line.select_additional_costs == 'transportation_costs')
                        legalized = sum(line.amount for line in sale_order.additional_costs_ids if
                                        line.select_additional_costs == 'legalized_documents')
                        client = sum(line.amount for line in sale_order.additional_costs_ids if
                                     line.select_additional_costs == 'client_commission')

                        commission = self.env['seller.commission'].create({
                            'agent_id': sale_order.user_id.id,
                            'sale_id': sale_order.id,
                            'amount_untaxed': sale_order.amount_untaxed,
                            'amount_tax': sale_order.amount_tax,
                            'amount_total': sale_order.amount_total,
                            'cost_total': cost,
                            'total': sale_order.commission_total,
                            'date_from': sale_order.date_order,
                            'supplier_invoice': supplier,
                            'guarantee_slip': guarantee,
                            'transportation_costs': transportation,
                            'legalized_documents': legalized,
                            'client_commission': client,
                            'state': 'draft',
                        })
                        sale_order.payment_comision = True
                        sale_order.payment_comision_id = commission.id

                        # Crear asiento contable de gastos si corresponde
                        sale_order.create_account_move_expenses(move)

        return res