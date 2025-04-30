from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            domain = [
                '|', '|', '|',
                ('partner_id.name', operator, name),  # <-- usamos .name no .display_name
                ('partner_name', operator, name),
                ('email_from', operator, name),
                ('contact_name', operator, name),
            ]
            leads = self.search(domain + args, limit=limit)
        else:
            leads = self.search(args, limit=limit)
        return leads.name_get()

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id and self.partner_id.user_id:
            self.user_id = self.partner_id.user_id