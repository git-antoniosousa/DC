from odoo import api, models, fields


class Aluno(models.Model):
    _name = "gest_diss.aluno"
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Aluno'
    _rec_name = "numero"

    partner_id = fields.Many2one('res.partner', required=True, ondelete="cascade")
    name = fields.Char(related='partner_id.name', inherited=True, readonly=False)
    email = fields.Char(related='partner_id.email', inherited=True, readonly=False)

    #nome = fields.Char(string="Nome")
    numero = fields.Char(string="Número")
    curso = fields.Many2one('gest_diss.curso', 'Curso')
    #email = fields.Char(string="Email")

    # ficha de um aluno pode ser um res partner

    def name_get(self):
        data = []
        for obj in self:
            f = f"({obj.numero}) {obj.name} | {obj.curso.codigo}"
            data.append((obj.id, f))
        return data

