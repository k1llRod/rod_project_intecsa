from odoo import api, fields, models, _
from odoo.exceptions import UserError
import io
import base64
import xlsxwriter
from datetime import datetime

class PartnerNoActivityWizard(models.TransientModel):
    _name = "partner.no.activity.wizard"
    _description = "Clientes sin actividad de cotizaciones (XLSX)"

    date_start = fields.Date(string="Fecha inicial", required=True)
    date_end = fields.Date(string="Fecha final", required=True)
    include_confirmed = fields.Boolean(
        string="Incluir pedidos confirmados como actividad",
        help="Si está marcado, también se consideran pedidos confirmados (state='sale') como actividad.",
        default=False,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Compañía",
        default=lambda self: self.env.company,
    )

    def action_export_xlsx(self):
        self.ensure_one()
        if self.date_start > self.date_end:
            raise UserError(_("La fecha inicial no puede ser mayor que la fecha final."))

        # Estados considerados "actividad"
        states = ["draft", "sent"]
        if self.include_confirmed:
            states.append("sale")
        states_tuple = tuple(states)

        # Alcance por compañía (incluye partners sin compañía)
        company_id = self.company_id.id if self.company_id else None

        params = {
            "date_start": f"{self.date_start} 00:00:00",
            "date_end": f"{self.date_end} 23:59:59",
            "states": states_tuple,
            "company_id": company_id,
        }

        # 1) Comercial partners con actividad de cotizaciones en el rango
        sql = """
            WITH partners_scope AS (
                SELECT p.id, p.commercial_partner_id
                FROM res_partner p
                WHERE p.active = TRUE
                  AND p.customer_rank > 0
                  AND (p.company_id = %(company_id)s OR p.company_id IS NULL)
            )
            SELECT ps.id
            FROM partners_scope ps
            WHERE NOT EXISTS (
                SELECT 1
                FROM sale_order so
                JOIN res_partner rp ON rp.id = so.partner_id
                WHERE rp.commercial_partner_id = ps.commercial_partner_id
                  AND so.state IN %(states)s
                  AND so.create_date >= %(date_start)s
                  AND so.create_date <= %(date_end)s
            );
        """
        self.env.cr.execute(sql, params)
        partner_ids = [r[0] for r in self.env.cr.fetchall()]

        # 2) Leemos datos útiles para el Excel
        fields_read = [
            "name", "commercial_company_name", "company_name",
            "vat", "email", "phone", "mobile",
            "country_id", "company_id", "user_id",
            "customer_rank", "create_date", "active",
            "commercial_partner_id",
        ]
        partners = self.env["res.partner"].sudo().browse(partner_ids).read(fields_read)

        # 3) (Opcional) última cotización del comercial partner (fuera de rango) para contexto
        # Mapa commercial_partner_id -> última fecha de cotización
        if partners:
            comm_ids = tuple({p["commercial_partner_id"][0] for p in partners if p.get("commercial_partner_id")})
            last_map = {}
            if comm_ids:
                self.env.cr.execute("""
                    SELECT rp.commercial_partner_id, MAX(so.create_date)
                    FROM sale_order so
                    JOIN res_partner rp ON rp.id = so.partner_id
                    WHERE rp.commercial_partner_id IN %s
                    GROUP BY rp.commercial_partner_id
                """, (comm_ids,))
                for row in self.env.cr.fetchall():
                    last_map[row[0]] = row[1]
        else:
            last_map = {}

        # 4) Construimos XLSX en memoria
        output = io.BytesIO()
        wb = xlsxwriter.Workbook(output, {"in_memory": True})
        ws = wb.add_worksheet("Sin actividad")

        fmt_title = wb.add_format({"bold": True})
        fmt_date = wb.add_format({"num_format": "yyyy-mm-dd hh:mm"})
        fmt_center = wb.add_format({"align": "center"})

        headers = [
            "ID", "Cliente", "Comercial (partner)", "NIT/VAT",
            "Email", "Teléfono", "Móvil",
            "País", "Vendedor", "Compañía",
            "Customer Rank", "Activo",
            "Creado (partner)", "Última cotización (global)",
            f"Rango consultado: {self.date_start} → {self.date_end}",
        ]

        for col, h in enumerate(headers):
            ws.write(0, col, h, fmt_title)

        row = 1
        for p in partners:
            country = p["country_id"][1] if p.get("country_id") else ""
            user = p["user_id"][1] if p.get("user_id") else ""
            comp = p["company_id"][1] if p.get("company_id") else ""
            comm = p["commercial_partner_id"][1] if p.get("commercial_partner_id") else ""

            last_q = ""
            if p.get("commercial_partner_id"):
                last_dt = last_map.get(p["commercial_partner_id"][0])
                if last_dt:
                    # convertir a tz del servidor (ya viene UTC); Excel formatea con fmt_date
                    try:
                        # parse ISO string si viene como str
                        if isinstance(last_dt, str):
                            last_dt = fields.Datetime.from_string(last_dt)
                    except Exception:
                        pass
                    last_q = last_dt

            ws.write(row, 0, p["id"])
            ws.write(row, 1, p["name"] or "")
            ws.write(row, 2, comm or "")
            ws.write(row, 3, p["vat"] or "")
            ws.write(row, 4, p["email"] or "")
            ws.write(row, 5, p["phone"] or "")
            ws.write(row, 6, p["mobile"] or "")
            ws.write(row, 7, country)
            ws.write(row, 8, user)
            ws.write(row, 9, comp)
            ws.write(row, 10, p.get("customer_rank", 0))
            ws.write(row, 11, "Sí" if p.get("active") else "No")
            # create_date
            cd = p.get("create_date")
            if isinstance(cd, str):
                try:
                    cd = fields.Datetime.from_string(cd)
                except Exception:
                    pass
            if cd:
                ws.write_datetime(row, 12, cd, fmt_date)
            else:
                ws.write(row, 12, "")
            # last quotation
            if last_q:
                ws.write_datetime(row, 13, last_q, fmt_date)
            else:
                ws.write(row, 13, "")
            # Col 14: rango (solo encabezado informativo)
            ws.write(row, 14, "")

            row += 1

        # Anchos
        ws.set_column(0, 0, 8)
        ws.set_column(1, 2, 32)
        ws.set_column(3, 6, 18)
        ws.set_column(7, 9, 18)
        ws.set_column(10, 11, 12)
        ws.set_column(12, 13, 20)
        ws.set_column(14, 14, 36)
        ws.freeze_panes(1, 0)

        wb.close()
        xlsx_data = output.getvalue()
        output.close()

        # 5) Guardamos como adjunto y devolvemos descarga
        filename = f"clientes_sin_actividad_{self.date_start}_{self.date_end}.xlsx"
        attachment = self.env["ir.attachment"].sudo().create({
            "name": filename,
            "type": "binary",
            "datas": base64.b64encode(xlsx_data),
            "res_model": "partner.no.activity.wizard",
            "res_id": self.id,
            "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        })

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=1",
            "target": "self",
        }
