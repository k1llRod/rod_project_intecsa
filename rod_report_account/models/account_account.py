from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class AccountAccount(models.Model):
    _inherit = 'account.account'

    account_category_id = fields.Many2one('account.category', string='Cuenta categoria')
    category_amount = fields.Float(string="Monto Categoria", compute='_calculate_category_amount', store=True)


    @api.depends('account_category_id')
    def _calculate_category_amount(self):
        for record in self:
            if record.current_balance > 0:
                record.category_amount = record.current_balance

            else:
                record.category_amount = 0




