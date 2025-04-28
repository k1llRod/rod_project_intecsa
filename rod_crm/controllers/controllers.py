# -*- coding: utf-8 -*-
# from odoo import http


# class RodCrm(http.Controller):
#     @http.route('/rod_crm/rod_crm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_crm/rod_crm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_crm.listing', {
#             'root': '/rod_crm/rod_crm',
#             'objects': http.request.env['rod_crm.rod_crm'].search([]),
#         })

#     @http.route('/rod_crm/rod_crm/objects/<model("rod_crm.rod_crm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_crm.object', {
#             'object': obj
#         })

