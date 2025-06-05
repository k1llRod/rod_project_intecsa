from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit ='sale.order'

    payment_comision = fields.Boolean(string='Pago de comisión', default=False)
    payment_comision_id = fields.Many2one('seller.commission', string='Pago de comisión')
    date_invoice = fields.Date(string='Fecha de factura', related='invoice_ids.invoice_date')
    payment_sale_id = fields.Many2one('account.payment', string='Pago de venta', copy=False)
    expense_move_id = fields.Many2one('account.move', string='Asiento de gastos', copy=False)
    def create_account_move_expenses(self):
        tax_rate = 0.13  # IVA 13%

        # Obtener cuentas desde la configuración
        account_guarantee_slip_ids = int(
            self.env['ir.config_parameter'].sudo().get_param('sales_config.account_guarantee_slip_ids', default=False))
        account_transportation_costs_ids = int(
            self.env['ir.config_parameter'].sudo().get_param('sales_config.account_transportation_expenses_ids',
                                                             default=False))
        account_legalized_documents_ids = int(
            self.env['ir.config_parameter'].sudo().get_param('sales_config.account_legalized_documents_ids',
                                                             default=False))
        account_client_commission_ids = int(
            self.env['ir.config_parameter'].sudo().get_param('sales_config.account_client_commission_ids',
                                                             default=False))
        account_supplier_invoice_ids = int(
            self.env['ir.config_parameter'].sudo().get_param('sales_config.account_supplier_invoice_ids',
                                                             default=False))
        account_base = int(
            self.env['ir.config_parameter'].sudo().get_param('sales_config.account_base', default=False))
        account_tax_expense = int(
            self.env['ir.config_parameter'].sudo().get_param('sales_config.account_tax_expense', default=False))
        journal_id = int(
            self.env['ir.config_parameter'].sudo().get_param('sales_config.journal_expense_id', default=False))

        for record in self:
            move_lines = []
            total_debit = 0.0
            total_credit = 0.0

            for rec in record.additional_costs_ids:
                selection_name = dict(rec.fields_get()['select_additional_costs']['selection'])[
                    rec.select_additional_costs]
                account_id = False

                if rec.select_additional_costs == 'supplier_invoice':
                    account_id = account_supplier_invoice_ids
                elif rec.select_additional_costs == 'guarantee_slip':
                    account_id = account_guarantee_slip_ids
                elif rec.select_additional_costs == 'transportation_costs':
                    account_id = account_transportation_costs_ids
                elif rec.select_additional_costs == 'legalized_documents':
                    account_id = account_legalized_documents_ids
                elif rec.select_additional_costs == 'client_commission':
                    account_id = account_client_commission_ids

                if account_id:
                    if rec.with_invoice:
                        base_amount = rec.amount / (1 + tax_rate)
                        tax_amount = rec.amount - base_amount
                    else:
                        base_amount = rec.amount
                        tax_amount = 0.0

                    # Gasto base (crédito)
                    move_lines.append((0, 0, {
                        'account_id': account_id,
                        'name': selection_name,
                        'debit': round(base_amount, 2),
                    }))
                    total_credit += base_amount

                    # Impuesto (crédito)
                    if tax_amount:
                        move_lines.append((0, 0, {
                            'account_id': account_tax_expense,
                            'name': f'IVA {selection_name}',
                            'debit': round(tax_amount, 2),
                        }))
                        total_credit += tax_amount

            if record.delivery_total:
                move_lines.append((0, 0, {
                    'account_id': account_base,
                    'name': 'Gastos adicionales',
                    'credit': round(record.delivery_total, 2),
                }))
                total_debit += record.delivery_total

            # Crear asiento contable separado
            if move_lines:
                move_vals = {
                    'ref': f"Gastos adicionales de {record.name}",
                    'journal_id': journal_id,
                    'date': fields.Date.context_today(self),
                    'line_ids': move_lines,
                }
                move = self.env['account.move'].create(move_vals)
                # move.action_post()  # Descomenta si deseas validar automáticamente
                record.expense_move_id = move.id
    def action_create_payment(self):
        self.ensure_one()
        invoice = self.invoice_ids.filtered(lambda x:x.state == 'posted')
        for rec in self:
            if invoice:
                # if invoice.filtered(lambda x: x.payment_ids):
                #     raise UserError("Esta factura ya tiene pagos registrados.")
                if invoice.filtered(lambda x: x.payment_state in ('in_payment', 'paid')):
                    raise UserError("La factura ya está pagada o tiene pagos en proceso.")

            rec.payment_comision = True
            supplier = sum(line.amount for line in rec.additional_costs_ids if line.select_additional_costs == 'supplier_invoice')
            guarantee = sum(line.amount for line in rec.additional_costs_ids if line.select_additional_costs == 'guarantee_slip')
            transportation = sum(line.amount for line in rec.additional_costs_ids if line.select_additional_costs == 'transportation_costs')
            legalized = sum(line.amount for line in rec.additional_costs_ids if line.select_additional_costs == 'legalized_documents')
            client = sum(line.amount for line in rec.additional_costs_ids if line.select_additional_costs == 'client_commission')
            cost = sum(line.standard_price * line.product_uom_qty for line in rec.order_line)

            journal_id = int(self.env['ir.config_parameter'].sudo().get_param('sales_config.payment_with_invoice', default=False))
            method_payment = self.env.ref('account.account_payment_method_manual_in')
            if not invoice:
                payment_vals = {
                    'payment_type': 'inbound',
                    'partner_type': 'customer',
                    'partner_id': rec.partner_id.id,
                    'amount': rec.amount_total,
                    # 'payment_method_line_id': method_payment.id,
                    'journal_id': journal_id,
                    'date': fields.Date.context_today(self),
                    'ref': f'Pago automático de {rec.name}',
                }
                payment_send = self.env['account.payment'].create(payment_vals)
                rec.payment_sale_id = payment_send.id
            # pago.action_post()

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
            if create_payment and rec.delivery_total > 0:
                expenses = rec.create_account_move_expenses()
