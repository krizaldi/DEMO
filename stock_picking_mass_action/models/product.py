# -*- coding: utf-8 -*-
from odoo import models, fields, api,_,exceptions
import base64
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
#from io import BytesIO
from pdf2image import convert_from_path, convert_from_bytes
import os
import re
from PyPDF2 import PdfFileMerger, PdfFileReader,PdfFileWriter
from io import BytesIO as StringIO
import base64
import datetime,time
from odoo.tools.mimetypes import guess_mimetype
import logging, ast
from odoo.tools import config, DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, pycompat
_logger = logging.getLogger(__name__)
import xml.etree.ElementTree as ET
from xml.dom import minidom

class compras(models.Model):
    _inherit = 'product.product'
    x_studio_color_bn = fields.Selection([('B/N','B/N'),('Color','Color')], string = 'Color - B/N', store = True)
    x_studio_color=fields.Selection([["Amarillo","Amarillo"],["Negro","Negro"],["Cian","Cian"],["Magenta","Magenta"]], store=True, string="Color")
    x_studio_toner_compatible=fields.Many2many('product.product',relation='product_product_rel', column1='id1',column2='id2', string="Compatibles")
    x_studio_rendimiento_toner=fields.Integer('Rendimiento')
    
    
    def agregarCompatible(self):
        wiz = self.env['add.compatible'].create({'productoInicial':self.id})
        view = self.env.ref('stock_picking_mass_action.view_addcompatile_action_form')
        return {
            'name': _('Agregar Compatibles'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'add.compatible',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': wiz.id,
            'context': self.env.context,
        }

class lots(models.Model):
    _inherit='stock.production.lot'
    x_studio_mini=fields.Boolean()
    x_studio_ultima_ubicacin=fields.Char(compute='cambio')
    x_studio_delegacion=fields.Char()
    x_studio_cambio=fields.Boolean()

    @api.depends('x_studio_cambio')
    def cambio(self):
        for r in self:
          tam=len(r.x_studio_move_line)
          pos=tam-1
          if(r.x_studio_localidad_2):
              loca=r.x_studio_localidad_2
              r['x_studio_ultima_ubicacin'] = str(loca.display_name)
              r['x_studio_delegacion']=str(loca.l10n_mx_edi_locality)
