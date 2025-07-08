from odoo import api, fields, models, tools, _
from odoo.osv.expression import AND

class WizardMayorBook(models.TransientModel):
    _name = 'wizard.mayor.book'
    _description = 'Wizard mayor book'

    name = fields.Char(string='ID aporte')
    date_start = fields.Date(string='Fecha inicial', default=fields.Datetime.now())
    date_end = fields.Date(string='Fecha Fin', default=fields.Datetime.now())
    account_id = fields.Many2many('account.account', string='Cuentas contables')
    # account_journal_id = fields.Many2one('account.journal', string='Diario')

    def report_mayor_book(self):
        data = {
            'date_start': self.date_start,
            'date_end': self.date_end,
            'account_id': self.account_id.code
        }
        return self.env.ref('rod_account.report_mayor_book').report_action(self, data=data)