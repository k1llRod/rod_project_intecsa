from odoo import fields, models, api, _

class ResUsers(models.Model):
    _inherit = 'res.users'

    commission_ids = fields.Many2one('commission', string='Comisiones')
    date = fields.Date(string='Fecha de asignacion', default=fields.Date.today)
    @api.model
    def create(self, values):
        res = super(ResUsers, self).create(values)
        if res.has_group('rod_sales.group_sales_manager'):
            res.commission_ids = self.env['commission'].search([('active', '=', True)], limit=1).id
        return res

    def assing_commission(self):
        self.partner_id.write({'commission_active': True})
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.partner_id.id,
            'views': [(False, 'form')],
            'target': 'new',
        }


