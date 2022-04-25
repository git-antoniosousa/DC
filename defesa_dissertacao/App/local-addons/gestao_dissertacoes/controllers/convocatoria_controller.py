from odoo import http
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime, timedelta
import pytz
from ics import Calendar, Event

class Convocatoria(http.Controller):

    @http.route('/convocatoria/<string:token>', auth='public')
    def get_processo(self, token,**kw):
        id = 4
        juri ='p'
        key = bytes(http.request.env['ir.config_parameter'].sudo().get_param('gest_diss.fernet_key',b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='), 'utf-8')
        fernet = Fernet(key)
        try:
            url = fernet.decrypt(token.encode()).decode()
        except InvalidToken:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 403,'msg': "Não tem acesso a este processo"})
        params = url.split("-/-")
        print(f"URL {url}")
        if len(params) < 3: return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo", 'header': "Convite para Júri de Prova de Defesa de Dissertação" })
        id = params[1]
        juri = params[0]
        if juri not in ['cp', 'cv', 'ca', 'cal']: return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo", 'header': "Convite para Júri de Prova de Defesa de Dissertação"})
        processo = http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)])
        print(f"PROCESS {processo} {kw.keys()} \n\n JURI {juri} {kw}"  )
        if processo:
            processo_resposta = processo
            local = pytz.timezone("Europe/Lisbon")
            data = datetime.strftime(pytz.utc.localize(datetime.strptime(str(processo.data_hora), "%Y-%m-%d %H:%M:%S")).astimezone(local),"%d/%m/%Y %H:%M %Z%z")
            data_inicio = datetime.strftime(datetime.strptime(str(processo.data_hora), "%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M")
            data_fim = datetime.strftime(datetime.strptime(str(processo.data_hora + timedelta(minutes=55)), "%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M")
            if(kw.get('convite')):
                http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)]).convocatoria(kw.get('convite'),juri)
                processo_resposta = http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)])
            if(juri == 'cp'):
                if processo.name != params[2]:
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo", 'header': "Convite para Júri de Prova de Defesa de Dissertação"})
                else :
                    if processo_resposta.convocatoria_presidente:
                        status = 1
                    else:
                        status = 0
                    print(f"STATUS {processo_resposta.convocatoria_presidente} {status} EXISTE {processo_resposta.juri_presidente_id}")
                    return http.request.render('gestao_dissertacoes.convocatoria', {'data': data,'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': status, 'existe': processo_resposta.juri_presidente_id})
            if(juri == 'cv'):
                if processo.name != params[2]:
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo", 'header': "Convite para Júri de Prova de Defesa de Dissertação"})
                else:
                    if processo_resposta.convocatoria_vogal:
                        status = 1
                    else:
                        status = 0
                    return http.request.render('gestao_dissertacoes.convocatoria', {'data': data,'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': status, 'existe': processo_resposta.juri_vogal_id})
            if(juri == 'ca'):
                if processo.name != params[2]:
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo", 'header': "Convite para Júri de Prova de Defesa de Dissertação"})
                else:
                    if processo_resposta.convocatoria_arguente:
                        status = 1
                    else:
                        status = 0
                    return http.request.render('gestao_dissertacoes.convocatoria', {'data': data,'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': status, 'existe': processo_resposta.juri_arguente_id})
            if (juri == 'cal'):
                if processo.name != params[2]:
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo", 'header': "Convite para Júri de Prova de Defesa de Dissertação"})
                else:
                    if processo_resposta.convocatoria_aluno:
                        status = 1
                    else:
                        status = 0
                    return http.request.render('gestao_dissertacoes.convocatoria', {'data': data,'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': status, 'existe': processo_resposta.juri_arguente_id})
                pass
        else:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado", 'header': "Convite para Júri de Prova de Defesa de Dissertação"})