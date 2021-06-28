from odoo import models
import logging, ast
import datetime, time
import xlsxwriter
import pytz
_logger = logging.getLogger(__name__)

class SolicitudesXlsx(models.AbstractModel):
    _name = 'report.solicitudes.report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, sale):
        i=2
        d=[]
        if(len(sale)==1 and sale.x_studio_arreglo!='/' and sale.x_studio_arreglo!=False):
            copia=sale
            #sale=self.env['sale.order'].browse(eval(sale.x_studio_arreglo)).filtered(lambda x:x.x_area_atencion==True)
            sale=self.env['sale.order'].browse(eval(sale.x_studio_arreglo)) 
            copia.write({'x_studio_arreglo':'/'})
        merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': 'blue'})
        report_name = 'Solicitudes'
        bold = workbook.add_format({'bold': True})
        sheet = workbook.add_worksheet('Solicitudes')
        sheet.merge_range('A1:P1', 'Solicitudes', merge_format)
        for obj in sale:
            equ=obj.order_line.filtered(lambda x:x.product_id.categ_id.id==13)
            if(len(equ)>1):
                for eq in equ:
                    sheet.write(i, 0, obj.name.replace('SO',''), bold)
                    sheet.write(i, 1, obj.date_order.strftime("%Y/%m/%d"), bold)
                    sheet.write(i, 2, obj.partner_id.name, bold)
                    sheet.write(i, 3, obj.x_studio_localidades, bold)
                    sheet.write(i, 4, obj.warehouse_id.name, bold)
                    sheet.write(i, 5, eq.x_studio_estado if eq.x_studio_estado else '', bold)
                    sheet.write(i, 6, eq.product_id.name, bold)
                    #m=self.env['stock.move.line'].search([['picking_id.sale_id','=',obj.id],['lot_id','=',eq.x_studio_field_9nQhR.id]]).lot_id.name
                    sheet.write(i, 7, str(eq.x_studio_field_9nQhR.name) if(eq.x_studio_field_9nQhR.name) else '', bold)
                    a=obj.order_line.filtered(lambda x:x.product_id.categ_id.id==11).mapped('product_id.name')
                    sheet.write(i, 8, str(a).replace('[','').replace(']','').replace('\'','') if(a!=[]) else '', bold)
                    b=obj.order_line.filtered(lambda x:x.product_id.categ_id.id==5).mapped('product_id.name')
                    sheet.write(i, 9, str(b).replace('[','').replace(']','').replace('\'','') if(b!=[]) else '', bold)
                    sheet.write(i, 10, len(obj.order_line.filtered(lambda x:x.product_id.categ_id.id==13).mapped('product_id.name')), bold)
                    sheet.write(i, 11, len(obj.order_line.filtered(lambda x:x.product_id.categ_id.id!=13).mapped('product_id.name')), bold)
                    sheet.write(i, 12, obj.x_studio_tipo_de_solicitud if(obj.x_studio_tipo_de_solicitud) else '', bold)
                    estado='Autorizada' if(obj.state=='sale') else str(obj.state)
                    sheet.write(i, 13, str(estado)+'/'+str(obj.write_uid.name), bold)
                    sheet.write(i, 14, obj.x_studio_usuario_creacion_1, bold)
                    #sheet.write(i, 15, 'Asignado' if(obj.x_studio_asignado) else 'No Asignado', bold)
                    sheet.write(i, 15, str(obj.note) if(obj.note) else '', bold)
                    sheet.write(i, 16, obj.validity_date.strftime("%Y/%m/%d") if(obj.validity_date) else '', bold)
                    i=i+1
            else:
                sheet.write(i, 0, obj.name.replace('SO',''), bold)
                sheet.write(i, 1, obj.date_order.strftime("%Y/%m/%d") if(obj.date_order) else '', bold)
                sheet.write(i, 2, obj.partner_id.name, bold)
                sheet.write(i, 3, obj.x_studio_localidades, bold)
                sheet.write(i, 4, obj.warehouse_id.name, bold)
                sheet.write(i, 5, equ.x_studio_estado if equ.x_studio_estado else '', bold)
                sheet.write(i, 6, equ.product_id.name, bold)
                #m=self.env['stock.move.line'].search([['picking_id.sale_id','=',obj.id],['lot_id','=',equ.x_studio_field_9nQhR.id]]).lot_id.name
                sheet.write(i, 7, str(equ.x_studio_field_9nQhR.name) if(equ.x_studio_field_9nQhR.id) else '', bold)
                a=obj.order_line.filtered(lambda x:x.product_id.categ_id.id==11).mapped('product_id.name')
                sheet.write(i, 8, str(a).replace('[','').replace(']','').replace('\'','') if(a!=[]) else '', bold)
                b=obj.order_line.filtered(lambda x:x.product_id.categ_id.id==5).mapped('product_id.name')
                sheet.write(i, 9, str(b).replace('[','').replace(']','').replace('\'','') if(b!=[]) else '', bold)
                sheet.write(i, 10, len(obj.order_line.filtered(lambda x:x.product_id.categ_id.id==13).mapped('product_id.name')), bold)
                sheet.write(i, 11, len(obj.order_line.filtered(lambda x:x.product_id.categ_id.id!=13).mapped('product_id.name')), bold)
                sheet.write(i, 12, obj.x_studio_tipo_de_solicitud if(obj.x_studio_tipo_de_solicitud) else '', bold)
                estado='Autorizada' if(obj.state=='sale') else str(obj.state)
                sheet.write(i, 13, str(estado)+'/'+str(obj.write_uid.name), bold)
                sheet.write(i, 14, obj.x_studio_usuario_creacion_1, bold)
                #sheet.write(i, 15, 'Asignado' if(obj.x_studio_asignado) else 'No Asignado', bold)
                sheet.write(i, 15, str(obj.note) if(obj.note) else '', bold)
                sheet.write(i, 16, obj.validity_date.strftime("%Y/%m/%d") if(obj.validity_date) else '', bold)
                i=i+1
        sheet.add_table('A2:P'+str(i),{'columns': [{'header': 'Numero de solicitud'},{'header': 'Fecha'},{'header': 'Cliente'},{'header':'Localidades'},{'header': 'Almacen'},{'header': 'Estado'},{'header': 'Modelo'},{'header': 'No. De serie'},{'header': 'Accesorio'},{'header': 'Toner'},{'header': 'Número de equipos'},{'header': 'Número de componentes'},{'header': 'Tipo'},{'header': 'Status'},{'header': 'Usuario Creación'},{'header': 'Comentarios'},{'header': 'Validez'}]}) 
        #sheet.add_table('A2:Q'+str(i),{'columns': [{'header': 'Numero de solicitud'},{'header': 'Fecha'},{'header': 'Cliente'},{'header':'Localidades'},{'header': 'Almacen'},{'header': 'Estado'},{'header': 'Modelo'},{'header': 'No. De serie'},{'header': 'Accesorio'},{'header': 'Toner'},{'header': 'Número de equipos'},{'header': 'Número de componentes'},{'header': 'Tipo'},{'header': 'Status'},{'header': 'Usuario Creación'},{'header': 'Asignado'},{'header': 'Comentarios'}]}) 
        workbook.close()