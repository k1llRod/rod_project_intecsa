# -*- coding: utf-8 -*-
# from odoo import http


# class RodCommission(http.Controller):
#     @http.route('/rod_commission/rod_commission', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_commission/rod_commission/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_commission.listing', {
#             'root': '/rod_commission/rod_commission',
#             'objects': http.request.env['rod_commission.rod_commission'].search([]),
#         })

#     @http.route('/rod_commission/rod_commission/objects/<model("rod_commission.rod_commission"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_commission.object', {
#             'object': obj
#         })

