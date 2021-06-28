# -*- coding: utf-8 -*-

from odoo import _, models, fields, api, tools
from email.utils import formataddr
from odoo.exceptions import UserError,RedirectWarning
from odoo import exceptions, _
import logging, ast
import datetime, time
_logger = logging.getLogger(__name__)

class DcasUpdate(models.Model):
	_inherit = 'product.product'
	#x_studio_color_bn = fields.Selection([('B/N','B/N'),('Color','Color')], string = 'Color - B/N', store = True)
	#x_studio_toner_compatible = fields.Many2many('product.product', relation = 'x_product_product_product_product_rel', column1 = 'id1', column2 = 'id2', string = "Toner compatible")

class ProductTemplate(models.Model):
	_inherit = 'product.template'
	x_studio_color_bn = fields.Selection([('B/N','B/N'),('Color','Color')], string = 'Color - B/N', store = True)
	x_studio_color = fields.Selection([["Amarillo","Amarillo"],["Negro","Negro"],["Cian","Cian"],["Magenta","Magenta"]], store=True, string="Color")
	x_studio_toner_compatible = fields.Many2many('product.product', relation = 'toner_compatible_rel', column1 = 'id1', column2 = 'id2', string = "Toner compatible")

     
