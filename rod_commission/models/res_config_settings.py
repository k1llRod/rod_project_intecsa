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
    journal_id = fields.Many2one(
        'account.journal',
        string="Diario de comisiones",
        help="Diario para el registro de comisiones."
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
        journal_id = IrConfigParam.sudo().get_param('sales_config.journal_id', default=False)
        res.update({
            'account_guarantee_slip_ids': int(account_id_1) if account_id_1 else False,
            'account_transportation_expenses_ids': int(account_id_2) if account_id_2 else False,
            'account_legalized_documents_ids': int(account_id_3) if account_id_3 else False,
            'account_client_commission_ids': int(account_id_4) if account_id_4 else False,
            'journal_id': int(journal_id) if journal_id else False,
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