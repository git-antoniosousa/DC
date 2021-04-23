from odoo import api, models, fields
from odoo.odoo.exceptions import ValidationError


class Processo(models.Model):

    _name = "gest_diss.processo"
    _description = 'Processo de gestão da dissertação'
    _rec_name = 'aluno_id'

    aluno_id = fields.Many2one('gest_diss.aluno', "Aluno")
    defesa_id = fields.Many2one('gest_diss.defesa', 'Defesa')
    juri_id = fields.Many2one('gest_diss.juri', 'Júri')

    orientador_id = fields.Many2one('gest_diss.docente', 'Orientador')
    coorientador_id = fields.Many2one('gest_diss.docente', 'Co-orientador')

    diss_titulo = fields.Char(string="Título")

    nota = fields.Integer(string="Nota")

    data_homologacao = fields.Date(string="Data de Homologação")

    estado = fields.Selection([
        ('registo_inicial', 'Registo Inicial'),
        ('correcoes', 'Correções'),
        ('proposta_juri', 'Proposta de Júri'),
        ('homologacao', 'Homologação'),
        ('ata_primeira_reuniao', 'Ata da Primeira Reunião'),
        ('declaracao_aluno', 'Declaração do Aluno'),
        ('ata_prova', 'Ata da Prova'),
        ('registo_nota', 'Registo de Nota'),
        ('aguardar_versao_final', 'A Aguardar Versão Final'),
        ('finalizado', 'Finalizado')
    ], string='Estado', readonly=True, copy=False, index=True, tracking=3, default='registo_inicial')

    def registo_aluno_action(self):
        if self.aluno_id is None or self.coorientador_id is None or self.orientador_id is None:
            raise ValidationError("Preencha o campo aluno e orientador e opcionalmente coorientador para registar o aluno.")
        else:
            return self.write({'estado': 'correcoes'})

    def correcoes_action(self):
        pass

    def prop_juri_action(self):
        pass

    def homologacao_action(self):
        pass

    def ata_primeira_reuniao_action(self):
        pass

    def declaracao_aluno_action(self):
        pass

    def ata_prova_action(self):
        pass

    def registo_nota_action(self):
        pass

    def aguardar_versao_final_action(self):
        pass

    def finalizar_action(self):
        pass

    def gerar_edital_action(self):
        x = 10

    def enviar_correcoes_action(self):
        pass
