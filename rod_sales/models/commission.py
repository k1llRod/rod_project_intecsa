from odoo import fields, models, api, _

class Commission(models.Model):
    _name = 'commission'
    _description = 'Comisión'

    name = fields.Char(string='Nombre', required=True)
    percentage = fields.Integer(string='Porcentaje', required=True)





