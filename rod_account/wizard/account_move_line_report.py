from odoo import models, api
from babel.numbers import format_decimal

class AccountMoveLineReport(models.AbstractModel):
    _name = 'report.rod_account.report_account_move_line'

    @api.model
    def _get_report_values(self, docids, data=None):
        sum_child = 0
        data_balance = []
        date_start = data['date_start']
        date_end = data['date_end']
        total_income = 0
        total_expense = 0
        total_income_historical = 0
        total_expense_historical = 0
        exercise_historical = 0
        sum_filtered_lines_historical = 0
        exercise = 0
        total_excercise = 0
        if data['type'] == 'income_statement':
            title = 'ESTADO DE RESULTADOS'
            account_category = self.env['account.account'].search([('account_category_id', '!=', False)]).filtered(
                lambda x: x.account_category_id.get_top_level_parent().result_status == True)

        if data['type'] == 'acoount_move_line':
            title = 'BALANCE GENERAL'
            account_category = self.env['account.account'].search([('account_category_id', '!=', False)]).filtered(
                lambda x: x.account_category_id.get_top_level_parent().balance_sheet == True)
        # lines = self.env['account.move.line'].search([
        #     ('date', '>=', date_start),
        #     ('date', '<=', date_end)
        # ])
        # filtered_lines = lines.filtered(lambda line: line.account_id.code.startswith(('4', '5')))
        # sum_filtered_lines = round(sum(filtered_lines.mapped('balance')),2)

        if data['type'] == 'income_statement':
            query = """
                SELECT 
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
                    AND aml.date BETWEEN %s and %s                        
                GROUP BY 
                    a.code, a.name, a.account_category_id
                order by a.code
            """
        if data['type'] == 'acoount_move_line':
            query = """
                    SELECT 
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
                        AND aml.date BETWEEN '2023-01-01' and %s                        
                    GROUP BY 
                        a.code, a.name, a.account_category_id
                    order by a.code
                """
        if data['type'] == 'acoount_move_line':
            self.env.cr.execute(query, (date_end,))
        if data['type'] == 'income_statement':
            self.env.cr.execute(query, (date_start, date_end))
        result = self.env.cr.fetchall()
        query_income = """
            SELECT 
                account_type.name AS tipo_cuenta,
                SUM(aml.debit) AS total_egresos,
                SUM(aml.credit) AS total_ingresos,
                SUM(aml.credit) - SUM(aml.debit) AS resultado_ejercicio
            FROM account_move_line aml
            JOIN account_account account ON aml.account_id = account.id
            JOIN account_account_type account_type ON account.user_type_id = account_type.id
            JOIN account_move move ON aml.move_id = move.id
            WHERE move.date BETWEEN %s AND %s
            AND move.state = 'posted'
            AND account_type.name IN ('Income', 'Expenses') 
            GROUP BY account_type.name;
            """
        query_historical = """
            SELECT 
                account_type.internal_group AS group_name,
                SUM(aml.debit) AS total_debit, 
                SUM(aml.credit) AS total_credit,
                SUM(aml.debit - aml.credit) AS total_balance
            FROM 
                account_move_line aml 
            LEFT JOIN 
                account_account account ON aml.account_id = account.id
            LEFT JOIN 
                account_account_type account_type ON account.user_type_id = account_type.id
            LEFT JOIN 
                account_move move ON aml.move_id = move.id
            WHERE 
                move.date BETWEEN '2023-01-01' AND %s
                AND move.state = 'posted'
                AND account_type.internal_group IN ('income', 'expense')
            GROUP BY 
                account_type.internal_group
            ORDER BY 
                account_type.internal_group;
        """
        self.env.cr.execute(query_income, (date_start, date_end))
        result_income = self.env.cr.fetchall()
        for data in result_income:
            if data[0] == 'Income':
                total_income = data[3]
            if data[0] == 'Expenses':
                total_expense = data[3]
                exercise = data[2]
        self.env.cr.execute(query_historical, (date_end,))
        result_historical = self.env.cr.fetchall()
        for data in result_historical:
            if data[0] == 'income':
                total_income_historical = data[3]
            if data[0] == 'expense':
                total_expense_historical =  data[3]
                exercise_historical = total_income_historical - total_expense_historical
        sum_filtered_lines_historical = round(total_income_historical + total_expense_historical, 2)
        sum_filtered_lines = total_income + total_expense
        for data in account_category:
            # if not data.account_category_id.get_top_level_parent():
            #     continue
            balance_total = 0
            fallback_balance = 0
            child = data.account_category_id.get_all_children()

            for rec in child:
                data_child = list(filter(lambda row: row[2] == rec.id, result))
                if data_child:
                    balance_total = balance_total + data_child[0][5]
            try:
                fallback_balance = list(filter(lambda row: row[2] == data.account_category_id.id, result))[0][5]
                fallback_balance = abs(fallback_balance)
            except IndexError:
                fallback_balance = 0
            balance_total = abs(balance_total)
            top_parent_str = data.account_category_id.parent_path.split('/')
            del top_parent_str[-1]
            top_parent_int = int(len(top_parent_str))
            if data.code == '3010301002':
                balance_total = abs(sum_filtered_lines)
            if data.account_category_id.header == True:
                if data.code == '1':
                    total_income = balance_total
                if data.code == '2':
                    total_expense = balance_total
                if data.code == '3':
                    exercise = total_income - total_expense
                    balance_total = balance_total + abs(sum_filtered_lines)
                    total_excercise = balance_total
                    if balance_total < 0:
                        fallback_balance = abs(balance_total)
                if data.code == '4':
                    total_income = balance_total
                if data.code == '5':
                    total_expense = balance_total
                    exercise = total_income - total_expense
            result_child = (
                data.code,
                data.name,
                0,
                0,
                # format_decimal(balance_total, locale='es_ES'),
                format_decimal(balance_total, locale='es_ES') if balance_total > 0 else format_decimal(fallback_balance, locale='es_ES'),
                data.deprecated,
                top_parent_int,
                data.account_category_id.header,
            )
            data_balance.append(result_child)
            # data_balance.append(result)
        a = 1
        return {
            'docs': data_balance,
            'title': title,
            'date_start': date_start,
            'date_end': date_end,
            'total_income': format_decimal(total_income, locale='es_ES'),
            'total_expense': format_decimal(total_expense, locale='es_ES'),
            'exercise': format_decimal(round(exercise, 2), locale='es_ES'),
            'total_excercise': format_decimal(total_expense + abs(round(exercise, 2)), locale='es_ES'),
            'sum_filtered_lines_historical': format_decimal(sum_filtered_lines_historical, locale='es_ES'),
            'self': self
        }

