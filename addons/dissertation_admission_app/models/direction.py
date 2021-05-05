from odoo import api, fields, models, exceptions
import logging

_logger = logging.getLogger(__name__)

class Direction(models.Model):
    _name = 'dissertation_admission.direction'
    _inherits = {'res.users': 'user_id'}
    _description = 'Secretaria de Curso'
    user_id = fields.Many2one('res.users', ondelete='restrict', required=True)
