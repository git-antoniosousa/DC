# -*- coding: utf-8 -*-

from odoo import models, fields, api
from validate_email import validate_email
from phonenumbers import is_valid_number, parse as parse_number


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Club Partner'
    _order = 'name'
    _rec_name = 'name'

    birthdate = fields.Date('Data de Nascimento')
    sexo = fields.Selection([('m', 'Masculino'),
                             ('f', 'Feminino'),
                             ('o', 'Outro')])
    isSocio = fields.Boolean('Sócio')

    @api.constrains('phone')
    @api.depends('phone')
    def _check_phone(self):
        for rec in self:
            if rec.phone and not is_valid_number(parse_number(rec.phone, 'PT')):
                raise models.ValidationError(
                    'O número de telefone \'{}\' não é um número português '
                    'válido.'.format(rec.phone))

    @api.constrains('email')
    @api.depends('email')
    def _check_email(self):
        for rec in self:
            if rec.email and not validate_email(rec.email):
                raise models.ValidationError(
                    'O email \'{}\' não é um email válido.'.format(rec.email))
