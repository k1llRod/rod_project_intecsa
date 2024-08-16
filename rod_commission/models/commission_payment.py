from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError

class CommissionPayment(models.Model):
    _name = 'commission.payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    total_commission = fields.Float(string='Total Commission', digits=(16, 2), track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='Vendedor', track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State', default='draft', track_visibility='onchange')
    date_from = fields.Date(string='Desde', track_visibility='onchange')
    date_to = fields.Date(string='Hasta', track_visibility='onchange')
    seller_ids = fields.One2many('seller.commission', 'commission_id', string='Comisiones')

    def action_payment(self):
        self.ensure_one()
        return {
            'name': 'Liquidar Comisión',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.commission.payment',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'default_user_id': self.agent_id.id,
                'default_total_commission': self.total_commission,
            },
        }

    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('commission.payment')
        vals['name'] = name
        res = super(CommissionPayment, self).create(vals)
        return res

    def register_payment(self):
        for record in self:
            if record.state == 'draft':
                record.write({'state': 'done'})

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise UserError(_('No puede eliminar una comisión liquidada'))
        return super(CommissionPayment, self).unlink()

    def register_draft(self):
        for record in self:
            if record.state == 'done':
                record.write({'state': 'draft'})

