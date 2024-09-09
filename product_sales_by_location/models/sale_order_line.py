# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Gayathri V (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    """Inheriting this model  to add new field."""
    _inherit = 'sale.order.line'

    line_location_id = fields.Many2one('stock.location',
                                       string='Location',
                                       domain="[('usage','=','internal')]",
                                       help=' Choose the location from'
                                            ' where the product taken from',
                                       default=lambda self: self.env.user.property_warehouse_id.view_location_id.id)

    warehouse_id = fields.Many2one('stock.warehouse', readonly=False)
    warehouse_ids = fields.Many2one('stock.warehouse', string='Almacen')

    @api.onchange('warehouse_ids')
    def _onchange_warehouse_ids(self):
        for record in self:
            record.warehouse_id = record.warehouse_ids.id

    @api.onchange('line_location_id')
    def _onchange_warehouse(self):
        for record in self:
            record.warehouse_ids = record.line_location_id.warehouse_id.id
            record.warehouse_ids = record.line_location_id.warehouse_id.id