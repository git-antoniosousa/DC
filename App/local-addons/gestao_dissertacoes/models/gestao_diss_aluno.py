from odoo import api, models, fields


class Aluno(models.Model):
    _name = "gest_diss.aluno"
    _description = 'Aluno'
    _rec_name = "numero"

    nome = fields.Char(string="Nome", required=True)
    numero = fields.Char(string="Número", required=True)
    curso = fields.Selection([('miei', 'MIEI'), ('miebiom', 'MIEBIOM')], required=True)
    email = fields.Char(string="Email")

    def name_get(self):
        data = []
        for obj in self:
            f = f"({obj.numero}) {obj.nome} | {obj.curso}"
            data.append((obj.id, f))
        return data

