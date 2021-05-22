# -*- coding: utf-8 -*-
from odoo import http
import os

import json
from openerp.http import request
from openerp.addons.web.controllers.main import serialize_exception,content_disposition
import base64
import PyPDF2 as pdf
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject

class GesJogo(http.Controller):

    def set_need_appearances_writer(self, writer):
        # See 12.7.2 and 7.7.2 for more information:
        # http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
        try:
            catalog = writer._root_object
            # get the AcroForm tree and add "/NeedAppearances attribute
            if "/AcroForm" not in catalog:
                writer._root_object.update({
                    NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

            need_appearances = NameObject("/NeedAppearances")
            writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
            return writer

        except Exception as e:
            print('set_need_appearances_writer() catch : ', repr(e))
            return writer

    @http.route('/web/binary/download_document', type='http', auth="user")
    @serialize_exception
    def download_document(self, model, id, info, filename=None, **kw):


        infojogo = json.loads(info)

        templateform = request.env['ir.config_parameter'].get_param("fpp_controlo_id","/tmp/Form_Controlo_Identidade.pdf")
        pdf_reader = pdf.PdfFileReader(open(templateform, 'rb'), strict=False)

        pdf_writer = pdf.PdfFileWriter()
        if "/AcroForm" in pdf_reader.trailer["/Root"]:
            pdf_reader.trailer["/Root"]["/AcroForm"].update(
                {NameObject("/NeedAppearances"): BooleanObject(True)})

        pdf_writer = pdf.PdfFileWriter()
        self.set_need_appearances_writer(pdf_writer)
        if "/AcroForm" in pdf_writer._root_object:
            pdf_writer._root_object["/AcroForm"].update(
                {NameObject("/NeedAppearances"): BooleanObject(True)})

        pdf_writer.addPage(pdf_reader.getPage(0))
        pdf_writer.updatePageFormFieldValues(pdf_writer.getPage(0), infojogo)

        outputStream = open(filename, "wb")
        pdf_writer.write(outputStream)

        # inputStream.close()
        outputStream.close()

        f = open(filename,'rb')
        content = f.read()
        #filename = '%s_%s' % (model.replace('.', '_'), id)
        f.close()
        os.unlink(filename)
        return request.make_response(content,
                                     [('Content-Type', 'application/x-pdf'),
                                      ('Content-Disposition', content_disposition(filename))])

    # class GestaoEquipas(http.Controller):
#     @http.route('/gestao_equipas/gestao_equipas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestao_equipas/gestao_equipas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestao_equipas.listing', {
#             'root': '/gestao_equipas/gestao_equipas',
#             'objects': http.request.env['gestao_equipas.gestao_equipas'].search([]),
#         })

#     @http.route('/gestao_equipas/gestao_equipas/objects/<model("gestao_equipas.gestao_equipas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestao_equipas.object', {
#             'object': obj
#         })