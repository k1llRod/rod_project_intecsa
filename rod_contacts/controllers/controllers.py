# -*- coding: utf-8 -*-
# from odoo import http


# class RodContacts(http.Controller):
#     @http.route('/rod_contacts/rod_contacts', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_contacts/rod_contacts/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_contacts.listing', {
#             'root': '/rod_contacts/rod_contacts',
#             'objects': http.request.env['rod_contacts.rod_contacts'].search([]),
#         })

#     @http.route('/rod_contacts/rod_contacts/objects/<model("rod_contacts.rod_contacts"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_contacts.object', {
#             'object': obj
#         })

