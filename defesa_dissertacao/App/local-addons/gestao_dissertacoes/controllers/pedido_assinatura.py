from odoo import http
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime, timedelta
import pytz
from ics import Calendar, Event
import base64

class PedidoAssinatura(http.Controller):


    @http.route('/declArguente/<string:token>', auth='public')
    def get_processo(self, token,**kw):
        key = bytes(http.request.env['ir.config_parameter'].sudo().get_param('gest_diss.fernet_key',
                                                               b'd7Jt7g7Cj3-we7PY_3Ym1mPH1U5Zx_KBQ69-WLhSD0w='), 'utf-8')

        fernet = Fernet(key)
        try:
            url = fernet.decrypt(token.encode()).decode()
        except InvalidToken:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 403,'msg': "Não tem acesso a este processo", 'header':"Declaração Arguente"})
        params = url.split("-/-")
        print(f"URL {url}")
        if len(params) < 3: return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado", 'header':"Declaração Arguente"})
        id = params[1]
        processo = http.request.env['gest_diss.processo'].sudo().search([('id', '=', id)])
        print(f"PROCESS {processo}")
        if processo:
            print(f"KW {kw}")
            processo_resposta = processo
            proc = http.request.env['gest_diss.processo'].sudo().browse(processo.id)
            if kw.get('decl_arguente', False):
                fname = kw.get('decl_arguente', False).filename
                file = kw.get('decl_arguente', False)
                data = file.read()

                proc.decl_arguente_assinada(data)
            return http.request.render('gestao_dissertacoes.justificacao_arguente', {'invite_processo': processo_resposta})
        else:
            return http.request.render('gestao_dissertacoes.not-found', {'code': 404 ,'msg': "Processo não encontrado", 'header':"Link de Video-Conferência para Prova"})