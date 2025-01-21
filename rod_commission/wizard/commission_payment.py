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
        if pay_commission:
            account_client_commission_ids = int(self.env['ir.config_parameter'].sudo().get_param('sales_config.account_client_commission_ids', default=False))
            journal_id = int(self.env['ir.config_parameter'].sudo().get_param('sales_config.journal_id', default=False))
            if not account_client_commission_ids or not journal_id:
                raise UserError(_('Debe configurar la cuenta contable de comisión de cliente y el diario de comisiones'))
            account_client_commission_ids = int(account_client_commission_ids)
            account_client_payable_id = self.user_id.partner_id.property_account_payable_id.id
            move_line_vals = [
                (0, 0, {  # Línea 1
                    'account_id': account_client_commission_ids,  # ID de la cuenta contable de débito
                    # 'name': "Descripción de la línea de débito",
                    'debit': self.total_commission,
                    'credit': 0.0,
                }),
                (0, 0, {  # Línea 2
                    'account_id': account_client_payable_id,  # ID de la cuenta contable de crédito
                    # 'name': "Descripción de la línea de crédito",
                    'debit': 0.0,
                    'credit': self.total_commission,
                }),
            ]

            # 3. Crear la cabecera del asiento (account.move)
            move_vals = {
                'journal_id': journal_id,
                'date': fields.Date.context_today(self),  # Fecha de hoy
                'ref': 'Ref Asiento Pago de comision',  # Referencia genérica o interna
                'line_ids': move_line_vals,  # Añadir las líneas
            }

            move = self.env['account.move'].create(move_vals)
            # 4. Validar (post) el asiento si deseas confirmarlo
            #    si lo dejas como draft, el usuario podrá revisarlo en borrador
            if move:
                pay_commission.account_move_id = move.id
                method = self.env['account.payment.method.line'].search([('name', '=', 'Manual')], limit=1)

                account_payment_id = self.env['account.payment'].create({
                    'payment_type': 'outbound',
                    'partner_id': self.user_id.partner_id.id,
                    'amount': self.total_commission,
                    'date': fields.Date.context_today(self),
                })
                if account_payment_id:
                    pay_commission.account_payment_id = account_payment_id.id
                    move.action_post()
                    return {
                        'name': 'Comisión liquidada',
                        'type': 'ir.actions.act_window',
                        'res_model': 'commission.payment',
                        'view_mode': 'form',
                        'view_type': 'form',
                        'res_id': pay_commission.id,
                        'target': 'current',
                    }
                    # account_payment_id.post()








