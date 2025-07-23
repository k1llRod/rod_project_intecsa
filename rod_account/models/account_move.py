from odoo import models, fields, api

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

    @api.depends('line_ids.debit', 'line_ids.credit')
    def _compute_totales(self):
        for move in self:
            move.total_debit = sum(move.line_ids.mapped('debit'))
            move.total_credit = sum(move.line_ids.mapped('credit'))