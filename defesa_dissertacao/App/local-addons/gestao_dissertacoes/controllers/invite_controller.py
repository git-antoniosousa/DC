from odoo import http
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime, timedelta
import pytz
from ics import Calendar, Event

class Invite(http.Controller):

    def ics_file(self, data_inicio, data_fim, local, numero, sala, name, link_vc=False):
        c = Calendar()
        e = Event()
        e.name = f"Prova de defesa dissertação - {numero} {name}"
        e.begin = data_inicio
        e.end = data_fim
        e.description = f"Prova de defesa de disseração de {numero} {name}"
        e.location = sala
        if link_vc != False:
            e.description = f"{e.description}\n link para a participação do arguente {link_vc}"
        #if local == 'presencial':
        #    e.description = "Defesa presencial da dissertação do aluno " + numero + " no "  + sala + " da Universidade do Minho"
        #if local == 'virtual':
        #    e.description = "Defesa virtual da dissertação do aluno " + numero + " através do link " + sala
        c.events.add(e)
        return str(c)

    @http.route('/invite/<string:token>', auth='public')
    def get_processo(self, token,**kw):
        id = 4
        juri ='p'
        key = bytes(http.request.env['ir.config_parameter'].sudo().get_param('gest_diss.fernet_key',b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='), 'utf-8')
        fernet = Fernet(key)
        try:
            url = fernet.decrypt(token.encode()).decode()
        except InvalidToken:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 403,'msg': "Não tem acesso a este processo (1)"})
        params = url.split("-/-")
        print(f"URL {url}")
        if len(params) < 3: return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processoi (2)", 'header': "Convite para Júri de Prova de Defesa de Dissertação" })
        id = params[1]
        juri = params[0]
        if juri not in ['p', 'v', 'a']: return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processoi (3)", 'header': "Convite para Júri de Prova de Defesa de Dissertação"})
        processo = http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)])
        print(f"PROCESS {processo} {kw.keys()} \n\n JURI {juri} {kw.get('enviar_decl_arguente')}"

              )
        if processo:
            processo_resposta = processo
            local = pytz.timezone("Europe/Lisbon")
            data = datetime.strftime(pytz.utc.localize(datetime.strptime(str(processo.data_hora), "%Y-%m-%d %H:%M:%S")).astimezone(local),"%d/%m/%Y %H:%M %Z%z")
            data_inicio = datetime.strftime(datetime.strptime(str(processo.data_hora), "%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M")
            data_fim = datetime.strftime(datetime.strptime(str(processo.data_hora + timedelta(minutes=55)), "%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M")
            ics = self.ics_file(data_inicio, data_fim, processo.local, processo.numero, processo.sala, processo.name, processo.link_vc)
            if(kw.get('convite')):
                http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)]).convite(kw.get('convite'),juri)
                processo_resposta = http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)])
            if(juri == 'p'):
                if processo.juri_presidente_id.name != params[2]: 
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo", 'header': "Convite para Júri de Prova de Defesa de Dissertação"})
                else : 
                    return http.request.render('gestao_dissertacoes.processo', {'ics': ics,'data': data,'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_presidente, 'existe': processo_resposta.juri_presidente_id})
            if(juri == 'v'):
                if processo.juri_vogal_id.name != params[2]:
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo", 'header': "Convite para Júri de Prova de Defesa de Dissertação"})
                else:
                    return http.request.render('gestao_dissertacoes.processo', {'ics': ics,'data': data,'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_vogal, 'existe': processo_resposta.juri_vogal_id})
            if(juri == 'a'):
                print(f"Atualizar declaracao {kw.get('enviar_decl_arguente')}")
                if kw.get('enviar_decl_arguente') != None:
                    print(f"Atualizar declaracao {kw.get('enviar_decl_arguente')}")
                    if kw.get('enviar_decl_arguente') == 'True':
                        http.request.env['gest_diss.processo'].sudo().browse(processo_resposta.id).enviar_decl_arguente=True
                    else:
                        http.request.env['gest_diss.processo'].sudo().browse(processo_resposta.id).enviar_decl_arguente = False

                        #.write(
                        #{'enviar_decl_arguente': kw.get('enviar_decl_arguente')})
                    print(f"{http.request.env['gest_diss.processo'].sudo().browse(processo_resposta.id).enviar_decl_arguente}")
                if processo.juri_arguente_id.name != params[2]: 
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo", 'header': "Convite para Júri de Prova de Defesa de Dissertação"})
                else:
                    return http.request.render('gestao_dissertacoes.processo', {'ics': ics,'data': data,'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_arguente, 'existe': processo_resposta.juri_arguente_id})
        else:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado", 'header': "Convite para Júri de Prova de Defesa de Dissertação"})
