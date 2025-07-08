from odoo import api, fields, models, tools, _
from odoo.osv.expression import AND

class WizardAccountReport(models.TransientModel):
    _name = 'wizard.account.report'
    _description = 'Wizard Account Report'

    name = fields.Char(string='ID aporte')
    date_start = fields.Date(string='Fecha inicial', default=fields.Datetime.now())
    date_end = fields.Date(string='Fecha Fin', default=fields.Datetime.now())
    type = fields.Char(string='Tipo de reporte')
    # account_journal_id = fields.Many2one('account.journal', string='Diario')

    def generate_pdf_report(self):
        query = '''
                SELECT 
                    move.id AS move_id,
                    move.date AS move_date,
                    line.debit AS debit,
                    line.credit AS credit,
                    line.balance AS balance
                FROM 
                    account_move_line AS line
                JOIN 
                    account_move AS move ON line.move_id = move.id
                WHERE
                    move.date >= '%s' AND move.date <= '%s'
                '''
        query = query % (self.date_start, self.date_end)

        self.env.cr.execute(query)
        data = self.env.cr.fetchall()
        context = {
            'report_data': data,
            'date_start': self.date_start,
            'date_end': self.date_end,
        }
        return self.env.ref('rod_account.custom_pdf_report').with_context(context).report_action(self, data=context)


    def report_account_move_line(self):
        type = 'acoount_move_line'
        data = {
            'date_start': self.date_start,
            'date_end': self.date_end,
            'type': type
        }
        return self.env.ref('rod_account.account_move_line_pdf_report').report_action(self, data=data)

    def report_income_statement(self):
        type = 'income_statement'
        data = {
            'date_start': self.date_start,
            'date_end': self.date_end,
            'type': type,
        }
        return self.env.ref('rod_account.account_move_line_pdf_report').report_action(self, data=data)

    def report_sums_balances(self):
        type = 'sums_balances'
        data = {
            'date_start': self.date_start,
            'date_end': self.date_end,
            'type': type,
        }
        return self.env.ref('rod_account.report_sums_balances').report_action(self, data=data)