import datetime
from datetime import timedelta, datetime
from odoo import models, api, fields
import pytz


class MapaReport(models.AbstractModel):
    _name = 'report.gestao_equipas.report_folha_convoc_evento_generate'


    def get_seccionistas_info(self, evento_desportivo):
        ttable =""
        tnames = list()
        for seccionista in evento_desportivo.seccionistas:
            #print(seccionista.licencas_desportivas, "**", seccionista.name)
            lic =''
            if seccionista.licencas_desportivas:
                lic = str(seccionista.licencas_desportivas[0].numero)
            ttable += '''<tr> 
            <td>
            ''' + str(seccionista.name) + '''
            </td>
            <td class="text-right" >
            ''' + lic + '''
            </td>
            </tr>
            '''
        return ttable

    def get_treinador_info(self, evento_desportivo):
        ttable =""
        tnames = list()
        for treinador in evento_desportivo.treinador:
            lic =''
            if treinador.licencas_desportivas:
                lic = str(treinador.licencas_desportivas[0].numero)
            ttable += '''<tr> 
            <td>
            ''' + str(treinador.name) + '''
            </td>
            <td class="text-right" >
            ''' + lic + '''
            </td>
            </tr>
            '''
        return ttable

    def get_adversario(self, evento_desportivo):
        adversario = str(evento_desportivo.equipa_adversaria.nome)
        return adversario

    def get_doc_cab(self, evento_desportivo):
        adversario = self.get_adversario(evento_desportivo)
        titulo = ''
        if evento_desportivo.em_casa == 's':
            titulo = "HCP vs "+ adversario
        else:
            titulo = adversario + " vs HCP"
        hd = '''<h2>Folha de convocatória '''+ titulo +'''</h2>'''
        return hd

    def get_info_jogo(self, evento_desportivo):
        antecedencia = evento_desportivo.antecedencia

        tz_local = pytz.timezone(self.env.user.partner_id.tz or 'UTC')
        inicio_naive = fields.Datetime.from_string(evento_desportivo.start)
        fim_naive = fields.Datetime.from_string(evento_desportivo.stop)
        apresentacao_naive = inicio_naive - timedelta(hours = antecedencia)


        dia = inicio_naive.strftime('%d/%m/%Y')
        inicio = (inicio_naive + timedelta(seconds = tz_local.utcoffset(inicio_naive).seconds) ).strftime('%H:%M')
        fim = (fim_naive + timedelta(seconds = tz_local.utcoffset(fim_naive).seconds) ).strftime('%H:%M')
        apresentacao = (apresentacao_naive + timedelta(seconds = tz_local.utcoffset(apresentacao_naive).seconds) ).strftime('%H:%M')




        if type(evento_desportivo.local.descricao) == bool:
            local = ""
        else:
            local = evento_desportivo.local.descricao

        competicao = str(evento_desportivo.competicao.designacao)
        adversario = str(evento_desportivo.equipa_adversaria.nome)
        numjogo = str(evento_desportivo.numero)
        if numjogo == False:
            numjogo =''
        epoca = str(evento_desportivo.epoca.name)

        info = '''
            <tr>
                <td>
                    <b>Época: </b>
                </td>
                <td>
                ''' + epoca + '''
                </td>
                <td>
                    <b>Competição: </b>
                </td>
                <td>
                ''' + competicao + '''
                </td>
            </tr>
            
            <tr>
                <td>
                    <b>Adversário: </b>
                </td>
                <td>
                ''' + adversario + '''
                </td>
                <td>
                    <b>Número de Jogo: </b>
                </td>
                <td>
                ''' + numjogo + '''
                </td>
            </tr>     
            <tr>
                <td>
                    <b>data: </b>
                </td>
                <td>
                ''' + dia + '''
                </td>
                <td>
                    <b>Local: </b>
                </td>
                <td>    
                    ''' + str(local) + '''
                </td>
            </tr>
            <tr>
                <td>
                    <b>Horário: </b>
                </td>
                <td>
                ''' + inicio + ''' - ''' + fim + ''' (''' + str(evento_desportivo.duracao) + ''' minutos)
                </td>
                <td>
                    <b>Hora Apresentação: </b>
                </td>
                <td>
                ''' + apresentacao + ''' 
                </td>

            </tr>
            <tr>
                <td>
                    <b>Escalão: </b>
                </td>
                <td>    
                ''' + str(evento_desportivo.escalao.designacao) + '''
                </td>
                <td>
                </td>
                <td>
                </td>
            </tr>
            <tr>
                <td>
                    <b>Treinador: </b>
                </td>
                <td>
                <table class="table table-bordered" style="margin-top: 10px;">
                    <thead>
                    <tr>
                        <th style="width: 20%;">Nome</th>
                        <th style="width: 10%;">Licença</th>
                    </tr>
                    </thead>
                    <tbody>
                ''' +  str(self.get_treinador_info(evento_desportivo))  + '''
                </tbody>
                <tfoot/>
                </table>
                </td>
                <td>
                    <b>Seccionistas: </b>
                </td>
                <td>
                <table class="table table-bordered" style="margin-top: 10px;">
                    <thead>
                    <tr>
                        <th style="width: 20;%">Nome</th>
                        <th style="width: 10%;">Licença</th>
                    </tr>
                    </thead>
                    <tbody>
                ''' +  str(self.get_seccionistas_info(evento_desportivo))  + '''
                </tbody>
                <tfoot/>
                </table>
                </td>
            </tr>
        '''
        return info

    def get_table_row(self, linha_convocatoria):
        row = '''
            <td>''' + linha_convocatoria.atleta.name + '''</td>
            <td class="text-right">''' + linha_convocatoria.atleta.licencas_desportivas[0].numero + '''</td>
            <td class="text-right" >''' \

        if linha_convocatoria.numero != 0:
              row += str(linha_convocatoria.numero)
        else:
            row += ''

        row += ''' </td>
            <td></td>
            <td></td>
        '''
        return row



    @api.model
    def get_report_values(self, doc_ids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        jogo = self.env['ges.jogo'].browse(data['jogo_id'])

        doc_args = {
            'doc_ids': doc_ids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            'jogo': jogo,
            'linhas_convocatoria': jogo.convocatorias,
            'get_info_jogo': self.get_info_jogo,
            'get_table_row': self.get_table_row,
            'get_doc_cab': self.get_doc_cab,
        }
        return doc_args
