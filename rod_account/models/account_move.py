from odoo import models, fields, api
from num2words import num2words

class AccountMove(models.Model):
    _inherit = 'account.move'

    total_debit = fields.Monetary(
        string='Total Débito',
        compute='_compute_totales',
        store=True,
        currency_field='currency_id'
    )
    total_credit = fields.Monetary(
        string='Total Crédito',
        compute='_compute_totales',
        store=True,
        currency_field='currency_id'
    )
    literal_number = fields.Char(string='Amount literal', compute='_compute_literal_number')
    @api.depends('line_ids.debit', 'line_ids.credit')
    def _compute_totales(self):
        for move in self:
            move.total_debit = sum(move.line_ids.mapped('debit'))
            move.total_credit = sum(move.line_ids.mapped('credit'))

    @api.depends('amount_total')
    def _compute_literal_number(self):
        for record in self:
            record.literal_number = num2words(int(record.amount_total), lang='es').upper()
            decimal = str(round(record.amount_total % 1 * 100))
            record.literal_number = record.literal_number + ', CON ' + decimal + '/100 BOLIVIANOS'

    def action_vr_send_to_middleware(self):
        for record in self:
            record.vr_send_to_middleware = False