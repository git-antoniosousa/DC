from odoo import http
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime, timedelta
import pytz
import base64
from ics import Calendar, Event

class Anexos(http.Controller):


    @http.route('/anexos/<string:token>', auth='public', methods=['POST', 'GET'],  website=True)
    def get_processo(self, token,**kw):

        key = bytes(http.request.env['ir.config_parameter']
                    .sudo().get_param('gest_diss.fernet_key',
                    b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='), 'utf-8')

        fernet = Fernet(key)
        try:
            url = fernet.decrypt(token.encode()).decode()
            print(f"ANEXOS {url}")
        except InvalidToken:
            print(f"ANEXOS invalid token  {token} ")
            return http.request.render('gestao_dissertacoes.not-found', {'code': 403,'msg': "Não tem acesso a este processo", 'header': "Anexos"})
        params = url.split("-/-")
        print(f"URL {url}")
        if len(params) < 3:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado", 'header': "Anexos"})
        id = params[1]
        processo = http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)])

        print(f"PROCESS ANEXOS {processo}")
        if processo:
            print(f"KW {kw}")
            processo_resposta = processo
            local = pytz.timezone("Europe/Lisbon")
            data = datetime.strftime(
                pytz.utc.localize(datetime.strptime(str(processo.data_hora), "%Y-%m-%d %H:%M:%S")).astimezone(local),
                "%d/%m/%Y %H:%M %Z%z")

            print(f"KW GET {kw.get('anexo5a', False)}")
            proc = http.request.env['gest_diss.processo'].sudo().browse(processo.id).processa_anexos_controller(kw)
            return http.request.render('gestao_dissertacoes.anexos', {'invite_processo': processo_resposta, 'data': data})
        else:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado", 'header': "Anexos"})