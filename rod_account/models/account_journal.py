from odoo import models, fields, api

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    title_report = fields.Char(string="Titulo comprobante")
    select_report = fields.Selection([('income','Ingreso'),('egress','Egreso')], string='Seleccionar comprobante')

