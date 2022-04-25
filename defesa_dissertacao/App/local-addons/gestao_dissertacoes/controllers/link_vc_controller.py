from odoo import http
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime, timedelta
import pytz
from ics import Calendar, Event

class LinkVC(http.Controller):


    @http.route('/linkvc/<string:token>', auth='public')
    def get_processo(self, token,**kw):
        key = bytes(http.request.env['ir.config_parameter'].sudo().get_param('gest_diss.fernet_key',
                                                               b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='), 'utf-8')

        fernet = Fernet(key)
        try:
            url = fernet.decrypt(token.encode()).decode()
        except InvalidToken:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 403,'msg': "Não tem acesso a este processo", 'header':"Link de Video-Conferência para Prova"})
        params = url.split("-/-")
        print(f"URL {url}")
        if len(params) < 3: return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado", 'header':"Link de Video-Conferência para Prova"})
        id = params[1]
        processo = http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)])
        print(f"PROCESS {processo}")
        if processo:
            print(f"KW {kw}")
            processo_resposta = processo
            local = pytz.timezone("Europe/Lisbon")
            data = datetime.strftime(
                pytz.utc.localize(datetime.strptime(str(processo.data_hora), "%Y-%m-%d %H:%M:%S")).astimezone(local),
                "%d/%m/%Y %H:%M %Z%z")

            if(kw.get('linkvc')):
                http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)]).update_link_vc(kw.get('linkvc'))
                processo_resposta = http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)])
            else:
                return http.request.render('gestao_dissertacoes.linkvc', {'invite_processo': processo_resposta, 'data': data})
        else:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado", 'header':"Link de Video-Conferência para Prova"})