from odoo import http
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime, timedelta
import pytz
from ics import Calendar, Event

class Invite(http.Controller):

    def ics_file(self, data_inicio, data_fim, local, numero, sala):
        c = Calendar()
        e = Event()
        e.name = "Defesa Dissertação - Aluno " + numero
        e.begin = data_inicio
        e.end = data_fim
        if local == 'presencial':
            e.description = "Defesa presencial da dissertação do aluno " + numero + " no "  + sala + " da Universidade do Minho" 
        if local == 'virtual':
            e.description = "Defesa virtual da dissertação do aluno " + numero + " através do link " + sala
        c.events.add(e)
        return str(c)

    @http.route('/invite/<string:token>', auth='public')
    def get_processo(self, token,**kw):
        id = 4
        juri ='p'
        fernet = Fernet(b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w=')
        try:
            url = fernet.decrypt(token.encode()).decode()
        except InvalidToken:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 403,'msg': "Não tem acesso a este processo"})
        params = url.split("-/-")
        print(f"URL {url}")
        if len(params) != 3: return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo"})
        id = params[1]
        juri = params[0]
        if juri not in ['p', 'v', 'a']: return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo"})
        processo = http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)])
        print(f"PROCESS {processo}")
        if processo:
            processo_resposta = processo
            local = pytz.timezone("Europe/Lisbon")
            data = datetime.strftime(pytz.utc.localize(datetime.strptime(str(processo.data_hora), "%Y-%m-%d %H:%M:%S")).astimezone(local),"%d/%m/%Y %H:%M %Z%z")
            data_inicio = datetime.strftime(datetime.strptime(str(processo.data_hora), "%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M")
            data_fim = datetime.strftime(datetime.strptime(str(processo.data_hora + timedelta(minutes=55)), "%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M")
            print(data_inicio)
            print(data_fim)
            ics = self.ics_file(data_inicio, data_fim, processo.local, processo.numero, processo.sala)
            print(ics)
            if(kw.get('convite')):
                http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)]).convite(kw.get('convite'),juri)
                processo_resposta = http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)])
            if(juri == 'p'):
                if processo.juri_presidente_id.name != params[2]: 
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo"})
                else : 
                    return http.request.render('gestao_dissertacoes.processo', {'ics': ics,'data': data,'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_presidente, 'existe': processo_resposta.juri_presidente_id})
            if(juri == 'v'):
                if processo.juri_vogal_id.name != params[2]: 
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo"})
                else:
                    return http.request.render('gestao_dissertacoes.processo', {'ics': ics,'data': data,'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_vogal, 'existe': processo_resposta.juri_vogal_id})
            if(juri == 'a'):
                if processo.juri_arguente_id.name != params[2]: 
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo"})
                else:
                    return http.request.render('gestao_dissertacoes.processo', {'ics': ics,'data': data,'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_arguente, 'existe': processo_resposta.juri_arguente_id})
        else:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado"})