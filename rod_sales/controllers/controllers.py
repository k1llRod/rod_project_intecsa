# -*- coding: utf-8 -*-
# from odoo import http


# class RodSales(http.Controller):
#     @http.route('/rod_sales/rod_sales', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_sales/rod_sales/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_sales.listing', {
#             'root': '/rod_sales/rod_sales',
#             'objects': http.request.env['rod_sales.rod_sales'].search([]),
#         })

#     @http.route('/rod_sales/rod_sales/objects/<model("rod_sales.rod_sales"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_sales.object', {
#             'object': obj
#         })

