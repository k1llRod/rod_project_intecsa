from odoo import models, fields, api

class TypeSale(models.Model):
    _name = 'type.sale'
    _description = 'Tipo de venta'

    name = fields.Char(string='Nombre', required=True)
    number_days = fields.Integer(string='Cantidad de dias', default=1)

