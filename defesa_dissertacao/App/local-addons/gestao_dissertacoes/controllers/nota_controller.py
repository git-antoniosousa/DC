from odoo import http
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime, timedelta
import pytz
import base64
from ics import Calendar, Event

class Anexos(http.Controller):


    @http.route('/nota/<string:token>', auth='public', methods=['POST', 'GET'],  website=True)
    def get_processo(self, token,**kw):

        key = bytes(http.request.env['ir.config_parameter']
                    .sudo().get_param('gest_diss.fernet_key',
                    b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='), 'utf-8')

        fernet = Fernet(key)
        try:
            url = fernet.decrypt(token.encode()).decode()
            print(f"NOTA {url}")
        except InvalidToken:
            print(f"Nota invalid token  {token} ")
            return http.request.render('gestao_dissertacoes.not-found', {'code': 403,'msg': "Não tem acesso a este processo", 'header': "Classificação Dissertação"})
        params = url.split("-/-")
        print(f"URL {url}")
        if len(params) < 3:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado", 'header': "Classificação Dissertação"})
        id = params[1]
        processo = http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)])
        print(f"PROCESS ANEXOS {processo}")
        if processo:
            print(f"KW GET {kw.get('anexo5a', False)}")
            atualizacao_diss = False
            if kw.get("atualizacao_diss", False):
                val = kw.get("atualizacao_diss")
                if val == 'SIM':
                    atualizacao_diss = True

            if kw.get("nota", False):
                nota = int(kw.get("nota", 0))
                if nota <10 or nota > 20:
                    return http.request.render('gestao_dissertacoes.notas', {'invite_processo': processo, 'message': "Nota Inválida"})
                else:
                    http.request.env['gest_diss.processo'].sudo().browse(processo.id).processa_notacontroller(atualizacao_diss, nota)

            return http.request.render('gestao_dissertacoes.notas', {'invite_processo': processo})
        else:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado"})