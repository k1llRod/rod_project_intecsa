from odoo import http
from odoo.http import request
from docx import Document
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
from docx.shared import Pt
from io import BytesIO

class SaleOrderReportController(http.Controller):

    @http.route('/sale_order/report/<int:order_id>', type='http', auth='user', website=True)
    def get_report(self, order_id):
        sale_order = request.env['sale.order'].browse(order_id)
        if not sale_order.exists():
            return request.not_found()

        # Generar el documento Word
        document = Document()
        document.add_heading('Reporte de Venta', level=1)
        document.add_paragraph(f'Orden: {sale_order.name}')
        document.add_paragraph(f'Fecha: {sale_order.date_order}')
        document.add_paragraph(f'Cliente: {sale_order.partner_id.name}')

        table = document.add_table(rows=1, cols=3)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Producto'
        hdr_cells[1].text = 'Cantidad'
        hdr_cells[2].text = 'Precio'

        for line in sale_order.order_line:
            row_cells = table.add_row().cells
            if line.display_type == False:
                row_cells[0].text = line.product_id.name
                row_cells[1].text = str(line.product_uom_qty)
                row_cells[2].text = str(line.price_unit)
            if line.display_type == 'line_note':
                row_cells[0].merge(row_cells[2])
                row_cells[0].text = line.name
                # row_cells[1].merge(row_cells[2])
                # row_cells[1].text = ''

        tbl = table._tbl
        for cell in tbl.iter_tcs():
            tc_pr = cell.tcPr
            borders = parse_xml(r'<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                                r'<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                                r'<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                                r'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                                r'<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                                r'</w:tcBorders>')
            tc_pr.append(borders)

        file_stream = BytesIO()
        document.save(file_stream)
        file_stream.seek(0)
        file_data = file_stream.read()

        # Crear y devolver la respuesta HTTP
        return request.make_response(
            file_data,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
                ('Content-Disposition', f'attachment; filename=Sales_Order_{sale_order.name}.docx')
            ]
        )

