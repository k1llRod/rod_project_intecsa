# -*- coding: utf-8 -*-
# from odoo import http


# class RodReportAccount(http.Controller):
#     @http.route('/rod_report_account/rod_report_account', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_report_account/rod_report_account/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_report_account.listing', {
#             'root': '/rod_report_account/rod_report_account',
#             'objects': http.request.env['rod_report_account.rod_report_account'].search([]),
#         })

#     @http.route('/rod_report_account/rod_report_account/objects/<model("rod_report_account.rod_report_account"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_report_account.object', {
#             'object': obj
#         })

