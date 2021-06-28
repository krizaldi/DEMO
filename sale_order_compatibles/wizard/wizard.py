from odoo import fields, api
from odoo.models import TransientModel
import logging, ast
import datetime, time
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
from odoo import exceptions, _




class AgregadosOdisminucion(TransientModel):
    _name = 'sale.agregado'
    _description = 'Sale order agregado'
    sale=fields.Many2one('sale.order')
    monto=fields.Float()
    bolsa=fields.Float()
    #tipoSolicitud=fields.Selection(related='sale.x_studio_tipo_de_solicitud')
    periodo=fields.Date()
    #servicio=fields.Many2one(related='sale.x_studio_field_69Boh')


    def agregar(self):
    	if(self.sale.x_studio_tipo_de_solicitud=="Retiro"):
    		self.sale.x_studio_field_69Boh.write({'bolsaCambio':float(self.sale.x_studio_field_69Boh.rentaMensual)-self.bolsa,'montoCambio':float(self.sale.x_studio_field_69Boh.rentaMensual)-self.monto,'fechaAplicacion':self.periodo})
    		self.sale.preparaSolicitud()
    	else:
    		self.sale.x_studio_field_69Boh.write({'bolsaCambio':float(self.sale.x_studio_field_69Boh.rentaMensual)+self.bolsa,'montoCambio':float(self.sale.x_studio_field_69Boh.rentaMensual)+self.monto,'fechaAplicacion':self.periodo})
    		self.sale.preparaSolicitud()

class SaleOrderMassAction(TransientModel):
    _name = 'sale.order.action'
    _description = 'Reporte de Solicitudes'
    fechaInicial=fields.Datetime()
    fechaFinal=fields.Datetime()
    tipo=fields.Selection([["Cambio","Cambio"],["Arrendamiento","Arrendamiento"],["Venta","Venta"],["Backup","Backup"],["Demostración","Demostración"],["Retiro","Retiro"],["Préstamo","Préstamo"]])
    def report(self):
        i=[]
        d=[]
        if(self.fechaInicial):
            m=['date_order','>=',self.fechaInicial]
            i.append(m)
        if(self.fechaFinal):
            m=['date_order','<=',self.fechaFinal]
            i.append(m)
        if(self.tipo):
            m=['x_studio_tipo_de_solicitud','=',self.tipo]
            i.append(m)
        i.append(['x_studio_field_bxHgp','=',False])
        d=self.env['sale.order'].search(i,order='date_order asc').filtered(lambda x:x.origin==False and x.x_studio_factura==False)
        if(len(d)>0):
            d[0].write({'x_studio_arreglo':str(d.mapped('id'))})
            return self.env.ref('stock_picking_mass_action.sale_xlsx').report_action(d[0])
        if(len(d)==0):
            raise UserError(_("No hay registros para la selecion actual"))