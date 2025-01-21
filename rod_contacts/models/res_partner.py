from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(tracking=True)
    area = fields.Char(string='Area / Seccion', tracking=True)
    name_contact = fields.Char(string='Nombre de contacto', tracking=True)
    mobile =  fields.Char(string='Movil', required=True, tracking=True)
    email = fields.Char(string='Correo electronico', required=False, tracking=True)

    @api.model
    def create(self, vals):
        if not vals.get('user_id'):
            vals['user_id'] = self.env.user.id
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].upper()
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].upper()
        return super(ResPartner, self).write(vals)
