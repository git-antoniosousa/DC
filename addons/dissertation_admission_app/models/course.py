from odoo import api, fields, models, exceptions
import logging


class Course(models.Model):
    _name = 'dissertation_admission.course'
    _description = 'Curso'
    name = fields.Char(required=True)