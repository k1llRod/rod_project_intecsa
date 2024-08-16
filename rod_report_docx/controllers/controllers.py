# -*- coding: utf-8 -*-
# from odoo import http


# class RodReportDocx(http.Controller):
#     @http.route('/rod_report_docx/rod_report_docx', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_report_docx/rod_report_docx/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_report_docx.listing', {
#             'root': '/rod_report_docx/rod_report_docx',
#             'objects': http.request.env['rod_report_docx.rod_report_docx'].search([]),
#         })

#     @http.route('/rod_report_docx/rod_report_docx/objects/<model("rod_report_docx.rod_report_docx"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_report_docx.object', {
#             'object': obj
#         })

