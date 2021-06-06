from odoo import http

class Invite(http.Controller):
    @http.route('/invite/<any(p,v,a):juri>/<int:id>/', auth='public')
    def get_processo(self, id, juri,**kw):
        processo = http.request.env['gest_diss.processo'].sudo().search([('id', 'ilike', id)]) 
        if processo:
            processo_resposta = processo
            if(kw.get('convite')):
                http.request.env['gest_diss.processo'].sudo().search([('id', 'ilike', id)]).convite(kw.get('convite'),juri)
                processo_resposta = http.request.env['gest_diss.processo'].sudo().search([('id', 'ilike', id)])
            if(juri == 'p'):
                return http.request.render('gestao_dissertacoes.processo', {'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_presidente, 'existe': processo_resposta.juri_presidente_id})
            if(juri == 'v'):
                return http.request.render('gestao_dissertacoes.processo', {'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_vogal, 'existe': processo_resposta.juri_vogal_id})
            if(juri == 'a'):
                return http.request.render('gestao_dissertacoes.processo', {'invite_processo': processo_resposta, 'tipo_juri': juri, 'status': processo_resposta.convite_arguente, 'existe': processo_resposta.juri_arguente_id})
        else:
            return http.request.render('gestao_dissertacoes.not-found')