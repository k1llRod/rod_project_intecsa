from odoo import models, api
from babel.numbers import format_decimal

class SumsBalances(models.AbstractModel):
    _name = 'report.rod_account.report_sums_balances_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        sum_child = 0
        data_balance = []
        title = 'Estado de resultados'
        data_balance = []
        date_start = data['date_start']
        date_end = data['date_end']
        query = """
                    SELECT 
                        a.code  AS account_code, 
                        a.name  AS account_name, 
                        a.account_type,
                        SUM(aml.debit)              AS total_debit, 
                        SUM(aml.credit)             AS total_credit,
                        SUM(aml.debit - aml.credit) AS balance
                    FROM account_move_line aml
                    JOIN account_account a ON aml.account_id = a.id
                    JOIN account_move am   ON aml.move_id   = am.id
                    WHERE am.state = 'posted'
                      AND aml.date >= '2025-01-01'     
                      AND aml.date <= %s     
                      AND a.internal_group NOT IN ('income', 'expense')
                    GROUP BY a.code, a.name, a.account_type
                    ORDER BY a.code;
                """
        self.env.cr.execute(query, (date_end, ))
        result = self.env.cr.fetchall()
        total_debit = 0
        total_credit = 0
        total_debtor = 0
        total_creditor = 0
        query_income_expenses = """
                    SELECT 
                        a.code  AS account_code, 
                        a.name  AS account_name, 
                        a.account_type,                  
                        SUM(aml.debit)  AS total_debit, 
                        SUM(aml.credit) AS total_credit,
                        SUM(aml.debit - aml.credit) AS balance
                    FROM account_move_line aml
                    JOIN account_account a ON aml.account_id = a.id
                    JOIN account_move am   ON aml.move_id   = am.id
                    WHERE am.state = 'posted'   
                      AND aml.date between %s and %s                                     
                      AND a.internal_group IN ('income','expense')
                    GROUP BY a.code, a.name, a.account_type
                    ORDER BY a.code;
                """
        self.env.cr.execute(query_income_expenses, (date_start, date_end))
        result_income_expenses = self.env.cr.fetchall()

        for record in result:
            result_child = (
                record[0],
                record[1],
                record[2],
                format_decimal(record[3], locale='es_ES'),
                format_decimal(record[4], locale='es_ES'),
                format_decimal(record[5], locale='es_ES') if record[5] > 0 else 0,
                format_decimal(abs(record[5]), locale='es_ES') if record[5] < 0 else 0
            )
            data_balance.append(result_child)
            total_debit += round(record[3],2)
            total_credit += round(record[4],2)
            total_debtor += round(record[5],2) if record[5] > 0 else 0
            total_creditor += abs(round(record[5],2)) if record[5] < 0 else 0

        for record in result_income_expenses:
            result_child = (
                record[0],
                record[1],
                record[2],
                format_decimal(record[3], locale='es_ES'),
                format_decimal(record[4], locale='es_ES'),
                format_decimal(record[5], locale='es_ES') if record[5] > 0 else 0,
                format_decimal(abs(record[5]), locale='es_ES') if record[5] < 0 else 0
            )
            data_balance.append(result_child)
            total_debit += round(record[3],2)
            total_credit += round(record[4],2)
            total_debtor += round(record[5],2) if record[5] > 0 else 0
            total_creditor += abs(round(record[5],2)) if record[5] < 0 else 0

        return {
            'docs': data_balance,
            'title': title,
            'date_start': date_start,
            'date_end': date_end,
            'self': self,
            'total_debit': format_decimal(total_debit, locale='es_ES'),
            'total_credit': format_decimal(total_credit, locale='es_ES'),
            'total_debtor': format_decimal(total_debtor, locale='es_ES'),
            'total_creditor': format_decimal(total_creditor, locale='es_ES'),
        }

