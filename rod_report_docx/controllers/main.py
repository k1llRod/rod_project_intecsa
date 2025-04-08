import os
from odoo import http
from odoo.http import request
from docx import Document
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
from docx.shared import Pt, Inches
from io import BytesIO
from docx.enum.text import WD_ALIGN_PARAGRAPH

import os
import base64
import io
class SaleOrderReportController(http.Controller):

    @http.route('/sale_order/report/<int:order_id>', type='http', auth='user', website=True)
    def get_report(self, order_id):
        sale_order = request.env['sale.order'].browse(order_id)
        env = request.env
        if not sale_order.exists():
            return request.not_found()

        # Generar el documento Word
        document = Document()
        # document.add_picture(image_stream, width=Inches(2))
        # Agregar encabezado con imagen
        section = document.sections[0]

        section.left_margin = Inches(0.4) #margen de hoja
        section.right_margin = Inches(0.4)
        header = section.header
        header_paragraph = header.paragraphs[0]
        module_path = os.path.dirname(os.path.abspath(__file__))
        # Ruta de la imagen (reemplazar con la ruta correcta o usar un stream si la imagen viene de la base de datos)
        # image_path = "custom_addons/rod_project_intecsa/rod_report_docx/static/src/img/intecsa.jpeg"
        # image_path_footer = "custom_addons/rod_project_intecsa/rod_report_docx/static/src/img/footer.png"
        image_path = os.path.join(module_path, '..', 'static', 'src', 'img', 'intecsa.jpeg')
        image_path_footer = os.path.join(module_path, '..', 'static', 'src', 'img', 'footer.png')
        header_paragraph.add_run().add_picture(image_path, width=Inches(1.25))
        # header_paragraph.add_run(f'Orden de entrega: {sale_order.name}')

        # Agregar pie de página
        footer = section.footer
        footer_paragraph = footer.paragraphs[0]
        footer_paragraph.add_run().add_picture(image_path_footer, width=Inches(7.5))

        document.add_heading('Orden de entrega', level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
        table_information = document.add_table(rows=1, cols=2)
        table_information.style = 'Table Grid'
        hdr_cells = table_information.rows[0].cells

        for rec in sale_order:
            # Nombre
            hdr_cells[0].paragraphs[0].add_run('Nombre').bold = True
            hdr_cells[1].text = rec.partner_id.name

            # NIT
            hdr_cells = table_information.add_row().cells
            hdr_cells[0].paragraphs[0].add_run('NIT').bold = True
            hdr_cells[1].text = rec.partner_id.vat if rec.partner_id.vat else ''

            # Dirección
            hdr_cells = table_information.add_row().cells
            hdr_cells[0].paragraphs[0].add_run('Dirección').bold = True
            hdr_cells[1].text = rec.partner_id.street if rec.partner_id.street else ''

            # Forma de pago
            hdr_cells = table_information.add_row().cells
            hdr_cells[0].paragraphs[0].add_run('Forma de pago').bold = True
            method =  rec.payment_method if rec.payment_method else ''
            if method == 'transfer':
                hdr_cells[1].text = 'Transferencia'
            elif method == 'transfer_sigep':
                hdr_cells[1].text = 'Transferencia SIGEP'
            elif method == 'cheque':
                hdr_cells[1].text = 'Cheque'
            elif method == 'qr':
                hdr_cells[1].text = 'QR'


            # Fecha de entrega
            hdr_cells = table_information.add_row().cells
            hdr_cells[0].paragraphs[0].add_run('Fecha de entrega').bold = True
            # hdr_cells[1].text = rec.delivery if rec.delivery else ''
            # hdr_cells = table_information.add_row().cells

        from docx.enum.table import WD_TABLE_ALIGNMENT
        for row in table_information.rows:
            for cell in row.cells:
                cell.vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
                # for paragraph in cell.paragraphs:
                #     paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        document.add_paragraph('')

        tbl1 = table_information._tbl
        for cell in tbl1.iter_tcs():
            tc_pr = cell.tcPr
            borders = parse_xml(r'<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                                r'<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                                r'<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                                r'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                                r'<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                                r'</w:tcBorders>')
            tc_pr.append(borders)


        table = document.add_table(rows=1, cols=4)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Producto'
        hdr_cells[1].text = 'Cantidad'
        hdr_cells[2].text = 'Precio unitario'
        hdr_cells[3].text = 'Precio total'

        for line in sale_order.order_line:
            row_cells = table.add_row().cells
            if line.display_type == False:
                row_cells[0].text = line.product_id.name
                row_cells[1].text = str(line.product_uom_qty)
                row_cells[2].text = str(line.price_unit)
                row_cells[3].text = str(line.price_total)
            if line.display_type == 'line_note':
                row_cells[0].merge(row_cells[3])
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

        document.add_paragraph('')
        document.add_heading('OBSERVACIONES', level=1)
        table_firmas = document.add_table(rows=1, cols=3)
        table_firmas.style = 'Table Grid'
        # tbl2 = table_firmas._tbl
        for record in sale_order:
            hdr_cells = table_firmas.rows[0].cells
            hdr_cells[0].text = '\n' + '\n' + '\n' + '\n'
            hdr_cells[1].text = '\n' + '\n' + '\n' + '\n'
            hdr_cells[2].text = '\n' + '\n' + '\n' + '\n'
            row_cells = table_firmas.add_row().cells
            row_cells[0].text = 'MANAGER OFFICE'
            paragraph = row_cells[0].paragraphs[0]
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].text = 'ASESOR COMERCIAL'
            paragraph = row_cells[1].paragraphs[0]
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[2].text = 'CLIENTE'
            paragraph = row_cells[2].paragraphs[0]
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells = table_firmas.add_row().cells
            row_cells[0].text = '\n' + 'Lic. Mario Robles M'
            paragraph = row_cells[0].paragraphs[0]
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].text =  '\n' + record.user_id.name
            paragraph = row_cells[1].paragraphs[0]
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[2].text = '\n' + 'Cargo:_________________________' + '\n' + 'Nombre:_________________________' + '\n'
            paragraph = row_cells[2].paragraphs[0]
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            # row_cells = table_firmas.add_row().cells

        tbl2 = table_firmas._tbl
        for cell in tbl2.iter_tcs():
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

