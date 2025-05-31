from odoo import _, api, fields, models
from odoo.exceptions import UserError
class SellerCommission(models.Model):
    _name = 'seller.commission'

    name = fields.Char(string='Codigo comision')
    agent_id = fields.Many2one('res.users', string='Vendedor')
    sale_id = fields.Many2one('sale.order', string='Orden de venta')
    date_from = fields.Date(string='Desde', store=True)
    date_to = fields.Date(string='Hasta', store=True)
    total = fields.Float(string='Comision')
    amount_untaxed = fields.Float(string='Base imponible')
    amount_tax = fields.Float(string='Impuestos')
    amount_total = fields.Float(string='Total')
    delivery_total = fields.Float(string='Total envio')
    cost_total = fields.Float(string='Costo total')
    margin = fields.Float(string='Margen')
    commission_id = fields.Many2one('commission.payment', string='Commission')
    supplier_invoice = fields.Float(string='Factura proveedor')
    guarantee_slip = fields.Float(string='Boleta Garantía')
    transportation_costs = fields.Float(string='Costos de transporte')
    legalized_documents = fields.Float(string='Documentos legalizados')
    client_commission = fields.Float(string='Comisión cliente')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State')
    def action_confirm(self):
        sum_commission = 0
        seller_ids = []
        agent = self.agent_id[0]
        date_from = self[0].date_from
        for rec in self:
            if rec.state == 'done':
                raise UserError(_('La comisión ya ha sido liquidada'))
            if date_from > rec.date_from:
                date_from = rec.date_from
            if agent.id == rec.agent_id.id:
                sum_commission = sum_commission + rec.total
                seller_ids.append(rec.id)
            else:
                raise UserError(_('No puede liquidar a dos agentes diferentes'))
        return {
            'name': 'Liquidar Comisión',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.commission.payment',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'default_user_id': agent.id,
                'default_total_commission': sum_commission,
                'default_seller_ids': seller_ids,
                'default_date_from' : date_from,
            }
        }

    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('seller.commission')
        vals['name'] = name
        res = super(SellerCommission, self).create(vals)
        return res

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise UserError(_('No puede eliminar una comisión liquidada'))
        return super(SellerCommission, self).unlink()

    def draft_massive(self):
        for rec in self:
            rec.state = 'draft'
