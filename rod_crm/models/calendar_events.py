from odoo import api, fields, models
from odoo.osv import expression

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def _default_partners(self):
        """ When active_model is res.partner, the current partners should be attendees """
        partners = self.env.user.partner_id
        active_id = self._context.get('active_id')
        if self._context.get('active_model') == 'res.partner' and active_id and active_id not in partners.ids:
            partners |= self.env['res.partner'].browse(active_id)
        return partners

    partner_ids = fields.Many2many('res.partner',
                                   'calendar_event_res_partner_rel',
                                   string='Asistentes',
                                   default=_default_partners,
                                   domain="[('user_ids', '!=', False)]")