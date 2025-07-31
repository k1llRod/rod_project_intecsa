from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(tracking=True)
    area = fields.Char(string='Area / Seccion', tracking=True)
    name_contact = fields.Char(string='Nombre de contacto', tracking=True)
    mobile =  fields.Char(string='Movil', required=True, tracking=True)
    email = fields.Char(string='Correo electronico', required=False, tracking=True)

    vat = fields.Char(string='NIT', required=False, tracking=True, default='0')

    _sql_constraints = [
        ('unique_mobile', 'UNIQUE(mobile)', 'Este número de celular ya está registrado.')
    ]
    @api.model
    def create(self, vals):
        if not vals.get('user_id'):
            vals['user_id'] = self.env.user.id
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].upper()
        if not vals.get('vat'):
            vals['vat'] = '0'
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].upper()
        # if not vals.get('vat'):
        #     if self.vat:
        #         vals['vat'] = '0'
        return super(ResPartner, self).write(vals)

    def unlink(self):
        if self.env.user.has_group('rod_contacts.group_no_delete_archive'):
            raise models.ValidationError("No tienes permisos para eliminar contactos.")
        return super(ResPartner, self).unlink()

    def toggle_active(self):
        if self.env.user.has_group('rod_contacts.group_no_delete_archive'):
            raise models.ValidationError("No tienes permisos para archivar contactos.")
        return super(ResPartner, self).toggle_active()

    @api.constrains('mobile')
    def _check_unique_mobile(self):
        for record in self:
            if record.mobile:
                existing = self.env['res.partner'].search([
                    ('mobile', '=', record.mobile),
                    ('id', '!=', record.id),
                    ('mobile', '!=', False)
                ], limit=1)
                if existing:
                    raise ValidationError("Este número de celular ya está registrado para otro contacto.")


