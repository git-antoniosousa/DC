from odoo import http
from cryptography.fernet import Fernet, InvalidToken

class Invite(http.Controller):
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
        print(url)
        if len(params) != 3: return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo"})
        id = params[1]
        juri = params[0]
        if juri not in ['p', 'v', 'a']: return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo"})
        processo = http.request.env['gest_diss.processo'].sudo().search([('id', 'ilike', id)]) 
        if processo:
            processo_resposta = processo
            if(kw.get('convite')):
                http.request.env['gest_diss.processo'].sudo().search([('id', 'ilike', id)]).convite(kw.get('convite'),juri)
                processo_resposta = http.request.env['gest_diss.processo'].sudo().search([('id', 'ilike', id)])
            if(juri == 'p'):
                if processo.juri_presidente_id.name != params[2]: 
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo"})
                else : 
                    return http.request.render('gestao_dissertacoes.processo', {'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_presidente, 'existe': processo_resposta.juri_presidente_id})
            if(juri == 'v'):
                if processo.juri_vogal_id.name != params[2]: 
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo"})
                else:
                    return http.request.render('gestao_dissertacoes.processo', {'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_vogal, 'existe': processo_resposta.juri_vogal_id})
            if(juri == 'a'):
                if processo.juri_arguente_id.name != params[2]: 
                    return http.request.render('gestao_dissertacoes.not-found', {'code': 403 ,'msg': "Não tem acesso a este processo"})
                else:
                    return http.request.render('gestao_dissertacoes.processo', {'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_arguente, 'existe': processo_resposta.juri_arguente_id})
        else:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado"})