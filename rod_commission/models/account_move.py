from odoo import models, fields, api, _
from datetime import datetime

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