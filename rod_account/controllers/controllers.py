# -*- coding: utf-8 -*-
# from odoo import http


# class RodAccount(http.Controller):
#     @http.route('/rod_account/rod_account', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_account/rod_account/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_account.listing', {
#             'root': '/rod_account/rod_account',
#             'objects': http.request.env['rod_account.rod_account'].search([]),
#         })

#     @http.route('/rod_account/rod_account/objects/<model("rod_account.rod_account"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_account.object', {
#             'object': obj
#         })

