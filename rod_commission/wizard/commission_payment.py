from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError

class CommissionPayment(models.TransientModel):
    _name = 'wizard.commission.payment'
    _description = 'Commission Payment'

    name = fields.Char(string='Name')
    total_commission = fields.Float(string='Total Commission', digits=(16, 2))
    user_id = fields.Many2one('res.users', string='Vendedor')
    date_from = fields.Date(string='Desde')
    date_to = fields.Date(string='Hasta')
    seller_ids = fields.Many2many('seller.commission', string='Comisiones')

    def action_payment(self):
        self.ensure_one()
        for rec in self.seller_ids:
            rec.date_to = self.date_to
            rec.state = 'done'
        seller_ids = self.seller_ids
        pay_commission = self.env['commission.payment'].create({
            'total_commission': self.total_commission,
            'user_id': self.user_id.id,
            'seller_ids': seller_ids,
            'date_from': self.date_from,
            'date_to': self.date_to,
        })




