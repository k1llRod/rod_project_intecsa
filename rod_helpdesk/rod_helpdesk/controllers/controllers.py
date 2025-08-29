# -*- coding: utf-8 -*-
# from odoo import http


# class RodHelpdesk(http.Controller):
#     @http.route('/rod_helpdesk/rod_helpdesk', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_helpdesk/rod_helpdesk/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_helpdesk.listing', {
#             'root': '/rod_helpdesk/rod_helpdesk',
#             'objects': http.request.env['rod_helpdesk.rod_helpdesk'].search([]),
#         })

#     @http.route('/rod_helpdesk/rod_helpdesk/objects/<model("rod_helpdesk.rod_helpdesk"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_helpdesk.object', {
#             'object': obj
#         })

