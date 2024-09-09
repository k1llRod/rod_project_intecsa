from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    area = fields.Char(string='Area / Seccion')
    name_contact = fields.Char(string='Nombre de contacto')
    mobile =  fields.Char(string='Movil', required=True)
    email = fields.Char(string='Correo electronico', required=False)