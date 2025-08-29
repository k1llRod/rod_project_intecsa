from odoo import models, api
from babel.numbers import format_decimal
from datetime import datetime

class MayorBookReport(models.AbstractModel):
    _name = 'report.rod_account.report_mayor_book_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        a = 1
        if data['account_id'] != False:
            query = """
                        SELECT 
                            a.code AS account_code, 
                            a.name AS account_name, 
                            a.account_category_id,
                            SUM(aml.debit) AS total_debit, 
                            SUM(aml.credit) AS total_credit,
                            SUM(aml.debit - aml.credit) AS balance,
                            TMP.balance AS before_balance,
                            (COALESCE(TMP.balance, 0) - SUM(aml.debit - aml.credit)) AS difference
                        FROM 
                            account_move_line aml
                        JOIN 
                            account_account a ON aml.account_id = a.id
                        JOIN 
                            account_move am ON aml.move_id = am.id
                        left join 
                            (SELECT 
                            a.code AS account_code, 
                            a.name AS account_name, 
                            a.account_category_id,
                            SUM(aml.debit) AS total_debit, 
                            SUM(aml.credit) AS total_credit,
                            SUM(aml.debit - aml.credit) AS balance
                        FROM 
                            account_move_line aml
                        JOIN 
                            account_account a ON aml.account_id = a.id
                        JOIN 
                            account_move am ON aml.move_id = am.id
                        WHERE 
                            am.state = 'posted'
                            AND aml.date BETWEEN '2023-01-01' AND %s
                        GROUP BY 
                            a.code, a.name, a.account_category_id
                        ORDER BY 
                            a.code)TMP on TMP.account_code = a.code
                        WHERE 
                            am.state = 'posted'
                            AND aml.date BETWEEN %s AND %s
                            AND a.code = %s
                        GROUP BY 
                            a.code, a.name, a.account_category_id, TMP.balance
                        ORDER BY 
                            a.code;
                    """
            self.env.cr.execute(query, (data['date_end'], data['date_start'], data['date_end'], data['account_id']))
        else:
            query = """
                    SELECT 
                        a.code AS account_code, 
                        a.name AS account_name, 
                        a.account_category_id,
                        SUM(aml.debit) AS total_debit, 
                        SUM(aml.credit) AS total_credit,
                        SUM(aml.debit - aml.credit) AS balance,
                        TMP.balance AS before_balance,
                        (COALESCE(TMP.balance, 0) - SUM(aml.debit - aml.credit)) AS difference
                    FROM 
                        account_move_line aml
                    JOIN 
                        account_account a ON aml.account_id = a.id
                    JOIN 
                        account_move am ON aml.move_id = am.id
                    left join 
                        (SELECT 
                        a.code AS account_code, 
                        a.name AS account_name, 
                        a.account_category_id,
                        SUM(aml.debit) AS total_debit, 
                        SUM(aml.credit) AS total_credit,
                        SUM(aml.debit - aml.credit) AS balance
                    FROM 
                        account_move_line aml
                    JOIN 
                        account_account a ON aml.account_id = a.id
                    JOIN 
                        account_move am ON aml.move_id = am.id
                    WHERE 
                        am.state = 'posted'
                        AND aml.date BETWEEN '2023-01-01' AND %s
                    GROUP BY 
                        a.code, a.name, a.account_category_id
                    ORDER BY 
                        a.code)TMP on TMP.account_code = a.code
                    WHERE 
                        am.state = 'posted'
                        AND aml.date BETWEEN %s AND %s
                    GROUP BY 
                        a.code, a.name, a.account_category_id, TMP.balance
                    ORDER BY 
                        a.code;
                """
            self.env.cr.execute(query, (data['date_end'],data['date_start'], data['date_end']))
        result_account = self.env.cr.fetchall()
        account_dict = {}
        for rec in result_account:
            account_dict[rec[0]] = {
                'code': rec[0],
                'account': rec[1],
                'debit': rec[3],
                'credit': rec[4],
                'balance': rec[5],
                'before_balance': rec[6],
                'difference': rec[7],
            }
        domain = [
            ('date', '>=', data['date_start']),
            ('date', '<=', data['date_end']),
        ]
        aml_records = self.env['account.move.line'].search(domain, order='account_id, date, move_id')
        if data['account_id']:
            aml_records = aml_records.filtered(lambda x:x.account_id.code == data['account_id'] and x.move_id.state == 'posted')

        ledger_data = {}
        for line in aml_records:
            account_id = line.account_id.id
            if account_id not in ledger_data:
                ledger_data[account_id] = {
                    'account_name': line.account_id.name,
                    'lines': [],
                    'total_debit': 0.0,
                    'total_credit': 0.0,
                    'code': line.account_id.code,
                    'total_balance': 0.0,
                    'difference': account_dict.get(line.account_id.code, 0)['difference'],
                    'before_total_balance': 0.0,
                }

            ledger_data[account_id]['lines'].append({
                'date': line.date,
                'journal': line.journal_id.name,
                'move_name': line.move_id.name,
                'partner': line.partner_id.name or '',
                'debit': line.debit,
                'credit': line.credit,
                'balance': 0.0,  # Se calculará luego
                'before_balance': 0.0,
                'ref': line.move_id.ref,
            })

            ledger_data[account_id]['total_debit'] += line.debit
            ledger_data[account_id]['total_credit'] += line.credit
            ledger_data[account_id]['total_balance'] += line.balance

        # Calcular el balance acumulado por cuenta
        for account_data in ledger_data.values():
            running_balance = 0.0
            for l in account_data['lines']:
                running_balance += (l['debit'] - l['credit'])
                l['balance'] = running_balance
                l['before_balance'] = round(account_dict.get(account_data['code'], 0)['difference'],2) + running_balance

        # === Formatear los valores con babel ===
        for account_id, account_data in ledger_data.items():
            # Convertir los totales en cadenas formateadas
            account_data['total_debit_str'] = format_decimal(
                account_data['total_debit'],
                format='#,##0.00',
                locale='es_ES'  # Ajusta según el locale deseado
            )
            account_data['total_credit_str'] = format_decimal(
                account_data['total_credit'],
                format='#,##0.00',
                locale='es_ES'
            )
            account_data['total_balance_str'] = format_decimal(
                account_data['total_balance'],
                format='#,##0.00',
                locale='es_ES'
            )

            # También podrías formatear cada línea si quieres
            for l in account_data['lines']:
                l['debit_str'] = format_decimal(l['debit'], format='#,##0.00', locale='es_ES')
                l['credit_str'] = format_decimal(l['credit'], format='#,##0.00', locale='es_ES')
                l['balance_str'] = format_decimal(l['balance'], format='#,##0.00', locale='es_ES')
                l['before_balance_str'] = format_decimal(l['before_balance'], format='#,##0.00', locale='es_ES')


        total_debit = round(ledger_data[account_id]['total_debit'],2)
        total_credit = round(ledger_data[account_id]['total_credit'],2)
        total_balance = round(ledger_data[account_id]['total_balance'],2)
        a = 1
        current_date = datetime.now().strftime('%d/%m/%Y')
        return {
            'docs': ledger_data,
            'date_start': data['date_start'],
            'date_end': data['date_end'],
            'current_date': current_date,
            'self': self,
        }
