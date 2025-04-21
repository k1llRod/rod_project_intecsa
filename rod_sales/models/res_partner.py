from odoo import fields, models, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    commission_ids = fields.Many2one('commission', string='Comisiones')
    date = fields.Date(string='Fecha de asignacion', default=fields.Date.today)
    commission_active = fields.Boolean(string='Activar comision', default=False)

    hide_peppol_fields = fields.Boolean(string='Ocultar campos Peppol', default=False)
    is_coa_installed = fields.Boolean(string='Chart of Accounts Installed', store=True)
