from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        res = super().action_create_payments()
        payments = self.env['account.payment'].search([('ref', '=', self.communication),('state', 'in', ['posted']) ], limit=1)
        sale_id = self.env['account.move'].search([('name','=',self.communication)], limit=1).invoice_origin
        sale = self.env['sale.order'].search([('name', '=', sale_id)], limit=1)
        if sale:
            for rec in sale:
                rec.payment_comision = True
                supplier = sum(line.amount for line in rec.additional_costs_ids if
                               line.select_additional_costs == 'supplier_invoice')
                guarantee = sum(line.amount for line in rec.additional_costs_ids if
                                line.select_additional_costs == 'guarantee_slip')
                transportation = sum(line.amount for line in rec.additional_costs_ids if
                                     line.select_additional_costs == 'transportation_costs')
                legalized = sum(line.amount for line in rec.additional_costs_ids if
                                line.select_additional_costs == 'legalized_documents')
                client = sum(line.amount for line in rec.additional_costs_ids if
                             line.select_additional_costs == 'client_commission')
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
                if not rec.expense_move_id or rec.expense_move_id.state == 'draft':
                    rec.expense_move_id.unlink()
                    expense = rec.create_account_move_expenses()
                # rec.expense_move_id = expense.id if expense else False
                rec.payment_sale_id = payments.id if payments else False

        return res
