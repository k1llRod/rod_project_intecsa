from odoo import models, fields, api

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    title_report = fields.Char(string="Titulo comprobante")

