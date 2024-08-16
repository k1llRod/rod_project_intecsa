# -*- coding: utf-8 -*-
# from odoo import http


# class RodPurchase(http.Controller):
#     @http.route('/rod_purchase/rod_purchase', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_purchase/rod_purchase/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_purchase.listing', {
#             'root': '/rod_purchase/rod_purchase',
#             'objects': http.request.env['rod_purchase.rod_purchase'].search([]),
#         })

#     @http.route('/rod_purchase/rod_purchase/objects/<model("rod_purchase.rod_purchase"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_purchase.object', {
#             'object': obj
#         })

