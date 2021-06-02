from odoo import api, models, fields


class Aluno(models.Model):
    _name = "gest_diss.aluno"
    _description = 'Aluno'
    _rec_name = "numero"

    nome = fields.Char(string="Nome")
    numero = fields.Char(string="Número")
    curso = fields.Many2one('gest_diss.curso', 'Curso')
    email = fields.Char(string="Email")

    # ficha de um aluno pode ser um res partner

    def name_get(self):
        data = []
        for obj in self:
            f = f"({obj.numero}) {obj.nome} | {obj.curso.nome}"
            data.append((obj.id, f))
        return data

