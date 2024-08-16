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