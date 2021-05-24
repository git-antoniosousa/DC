# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CategoriaTreino(models.Model):
    _name = 'ges.categoria_treino'
    _description = 'Categoria de Treino'
    _order = 'name'
    _parent_store = True

    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)

    display_name = fields.Char("Nome")
    name = fields.Char('Designação', required=True)
    parent_id = fields.Many2one('ges.categoria_treino', 'Super-Categoria',
                                ondelete='restrict', index=True)
    child_ids = fields.One2many('ges.categoria_treino', 'parent_id',
                                string='Sub-Categorias')

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Não é possível criar categorias '
                                         'recursivas.')

    @api.multi
    @api.depends('name')
    def name_get(self):
        repr = []
        for record in self:
            novo_nome = record.name
            record_actual = record

            while record_actual.parent_id.name:
                novo_nome = record_actual.parent_id.name + " > " + novo_nome
                record_actual = record_actual.parent_id

            repr.append((record.id, novo_nome))
        return repr
