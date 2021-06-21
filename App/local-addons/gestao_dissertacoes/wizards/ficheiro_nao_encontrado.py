from odoo import fields, models


class StateErrorMessage(models.TransientModel):
    _name = 'gest.ficheiro_nao_encontrado.wizard'
    _description = 'Ficheiro Não Encontrado'

    message = fields.Text(string="O ficheiro para anexar ao email não foi encontrado. Verifique se o ficheiro existe ou se tem o nome correto.", readonly=True, store=False)
