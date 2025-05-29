from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

class AccountCategory(models.Model):
    _name = 'account.category'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char('Name', index=True, required=True)
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name', recursive=True,
        store=True)
    parent_id = fields.Many2one('account.category', 'Parent Category', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    header = fields.Boolean(string="Encabezado")
    child_id = fields.One2many('account.category', 'parent_id', 'Child Categories')
    balance_sheet = fields.Boolean(string="Balanace general")
    result_status = fields.Boolean(string="Estado de resultados")

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    def get_all_children(self):
        """
        Devuelve una lista de IDs de todos los hijos (y sus hijos) recursivamente.
        """
        all_children = self.env['account.category'].browse()  # Inicializa una lista vacía de registros
        for category in self:
            all_children |= category.child_id
            all_children |= category.child_id.get_all_children()
        return all_children

    def get_top_level_parent(self):
        """
        Devuelve el ancestro más alto (padre de padres) de la categoría actual.
        Si la categoría no tiene padre, se retorna a sí misma.
        """
        self.ensure_one()
        category = self
        while category.parent_id:
            category = category.parent_id
        return category

