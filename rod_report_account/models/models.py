# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rod_report_account(models.Model):
#     _name = 'rod_report_account.rod_report_account'
#     _description = 'rod_report_account.rod_report_account'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

