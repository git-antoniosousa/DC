from odoo import api, models, fields


class Aluno(models.Model):
    _name = "gest_diss.aluno"
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Aluno'
    _rec_name = "numero"



    partner_id = fields.Many2one('res.partner', required=True, ondelete="restrict")
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

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        print(f"on change partner {self.email} {self.partner_id}")
        if self.email == False:
            return
        model = self.env['dissertation_admission.student']
        res = self.env['res.users'].search([('email', '=', self.email)])
        print(f"{res}")
        if len(res) != 0:
            res1 = model.search([('user_id','=', res[0].id)])
            print(f"res1 {res1} {res[0].id} {res[0]}")
            if len(res1) != 0:
                self.curso = res1[0].course
                self.numero = res1[0].university_id
                plano = self.env['dissertation_admission.work_plan'].search([('student.id','=',res1[0].id )])
                if len(plano) != 0:
                    pass
        return