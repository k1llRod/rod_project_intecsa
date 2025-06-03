from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    account_guarantee_slip_ids = fields.Many2one(
        'account.account',
        string="Cuenta de boleta de garantia",
        help="Cuenta contable para el primer ingreso extra en ventas."
    )
    account_transportation_expenses_ids = fields.Many2one(
        'account.account',
        string="Cuenta de gastos de transporte",
        help="Cuenta contable para el segundo ingreso extra en ventas."
    )
    account_legalized_documents_ids = fields.Many2one(
        'account.account',
        string="Cuenta de documentos legalizados",
        help="Cuenta contable para el tercer ingreso extra en ventas."
    )
    account_client_commission_ids = fields.Many2one(
        'account.account',
        string="Cuenta de comision de cliente",
        help="Cuenta contable para el cuarto ingreso extra en ventas."
    )
    account_supplier_invoice_ids = fields.Many2one(
        'account.account',
        string="Cuenta de factura de proveedor",
        help="Cuenta contable para la factura de proveedor en ventas."
    )
    account_base = fields.Many2one(
        'account.account',
        string="Cuenta base de gastos",
        help="Cuenta contable base para los gastos extra en ventas."
    )
    journal_id = fields.Many2one(
        'account.journal',
        string="Diario de comisiones",
        help="Diario para el registro de comisiones."
    )
    payment_with_invoice = fields.Many2one(
        'account.journal',
        string="Diario de pago sin factura",
        help="Diario utilizado para registrar pagos sin factura."
    )
    account_tax_expense = fields.Many2one(
        'account.account',
        string="Cuenta de impuesto de gastos",
        help="Cuenta contable para el impuesto aplicado a los gastos."
    )
    journal_expense_id = fields.Many2one(
        'account.journal',
        string="Diario de gastos",
        help="Diario utilizado para registrar los gastos adicionales."
    )

    @api.model
    def get_values(self):
        """
        Lee los valores desde ir.config_parameter y
        los asigna a los campos Many2one.
        """
        res = super(ResConfigSettings, self).get_values()
        IrConfigParam = self.env['ir.config_parameter']

        account_id_1 = IrConfigParam.sudo().get_param('sales_config.account_guarantee_slip_ids', default=False)
        account_id_2 = IrConfigParam.sudo().get_param('sales_config.account_transportation_expenses_ids', default=False)
        account_id_3 = IrConfigParam.sudo().get_param('sales_config.account_legalized_documents_ids', default=False)
        account_id_4 = IrConfigParam.sudo().get_param('sales_config.account_client_commission_ids', default=False)
        account_id_5 = IrConfigParam.sudo().get_param('sales_config.account_supplier_invoice_ids', default=False)
        account_base = IrConfigParam.sudo().get_param('sales_config.account_base', default=False)
        journal_id = IrConfigParam.sudo().get_param('sales_config.journal_id', default=False)
        journal_expense_id = IrConfigParam.sudo().get_param('sales_config.journal_expense_id', default=False)
        payment_with_invoice = IrConfigParam.sudo().get_param('sales_config.payment_with_invoice', default=False)
        account_id_6 = IrConfigParam.sudo().get_param('sales_config.account_tax_expense', default=False)
        res.update({
            'account_guarantee_slip_ids': int(account_id_1) if account_id_1 else False,
            'account_transportation_expenses_ids': int(account_id_2) if account_id_2 else False,
            'account_legalized_documents_ids': int(account_id_3) if account_id_3 else False,
            'account_client_commission_ids': int(account_id_4) if account_id_4 else False,
            'journal_id': int(journal_id) if journal_id else False,
            'account_base': int(account_base) or False,
            'account_supplier_invoice_ids': int(account_id_5) if account_id_5 else False,
            'payment_with_invoice': int(payment_with_invoice) if payment_with_invoice else False,
            'account_tax_expense': int(account_id_6) if account_id_6 else False,
            'journal_expense_id': int(journal_expense_id) if journal_expense_id else False,
        })
        return res

    def set_values(self):
        """
        Almacena los valores en ir.config_parameter
        para que persistan en la configuración.
        """
        super(ResConfigSettings, self).set_values()
        IrConfigParam = self.env['ir.config_parameter'].sudo()

        IrConfigParam.set_param('sales_config.account_guarantee_slip_ids', self.account_guarantee_slip_ids.id or False)
        IrConfigParam.set_param('sales_config.account_transportation_expenses_ids', self.account_transportation_expenses_ids.id or False)
        IrConfigParam.set_param('sales_config.account_legalized_documents_ids', self.account_legalized_documents_ids.id or False)
        IrConfigParam.set_param('sales_config.account_client_commission_ids',self.account_client_commission_ids.id or False)
        IrConfigParam.set_param('sales_config.journal_id', self.journal_id.id or False)
        IrConfigParam.set_param('sales_config.payment_with_invoice', self.payment_with_invoice.id or False)
        IrConfigParam.set_param('sales_config.account_base', self.account_base.id or False)
        IrConfigParam.set_param('sales_config.account_supplier_invoice_ids', self.account_supplier_invoice_ids.id or False)
        IrConfigParam.set_param('sales_config.account_tax_expense', self.account_tax_expense.id or False)
        IrConfigParam.set_param('sales_config.journal_expense_id', self.journal_expense_id.id or False)