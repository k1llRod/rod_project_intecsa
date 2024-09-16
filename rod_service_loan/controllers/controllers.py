# -*- coding: utf-8 -*-
# from odoo import http


# class RodServiceLoan(http.Controller):
#     @http.route('/rod_service_loan/rod_service_loan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_service_loan/rod_service_loan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_service_loan.listing', {
#             'root': '/rod_service_loan/rod_service_loan',
#             'objects': http.request.env['rod_service_loan.rod_service_loan'].search([]),
#         })

#     @http.route('/rod_service_loan/rod_service_loan/objects/<model("rod_service_loan.rod_service_loan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_service_loan.object', {
#             'object': obj
#         })

