from odoo import models, fields, api
from odoo.exceptions import UserError

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def open_wizard_change_cost(self):
        """
        Abre el asistente para cambiar el costo de los productos seleccionados.
        """
        a = 1
        return {
            'name': 'Cambiar costo',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.inventory.product',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_quants_id': self.ids,
            }
        }