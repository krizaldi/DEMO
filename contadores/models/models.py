# -*- coding: utf-8 -*-
from odoo import models, fields, api
import base64,io,csv
import logging, ast
import datetime
import xlsxwriter 
import base64
import csv
import json
from odoo.exceptions import UserError
from odoo import exceptions, _
from operator import concat
_logger = logging.getLogger(__name__)






def get_years():
    year_list = []
    for i in range(2010, 2036):
       year_list.append((str(i), str(i)))
    return year_list
valores = [('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), ('04', 'Abril'),
                          ('05', 'Mayo'), ('06', 'Junio'), ('07', 'Julio'), ('08', 'Agosto'),
                          ('09', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')]



class dcas(models.Model):
    _name = 'dcas.dcas'
    _description ='DCAS'
    _inherit = ['mail.thread', 'mail.activity.mixin']    
    name = fields.Char()
    active = fields.Boolean(string = 'Active', default = True)
    dispositivo = fields.Char()
    ultimoInforme=fields.Datetime('Ultimo Informe')
    respaldo=fields.Boolean(string='Respaldo')
    usb=fields.Boolean(string='Usb')
    serie_aux=fields.Char()
    serie=fields.Many2one('stock.production.lot',string='Numero de Serie')
    grupo_aux=fields.Char()
    grupo=fields.Many2one('res.partner',store=True)
    ubicacion=fields.Char()
    ip=fields.Char(string='IP')
    contadorColor=fields.Integer(string='Contador Color',track_visibility='onchange')
    contadorMono=fields.Integer(string='Contador Monocromatico',track_visibility='onchange')
    contador_id=fields.Many2one('contadores.contadores')        
    dominio=fields.Integer()
    porcentajeNegro=fields.Integer(string='Negro')
    porcentajeAmarillo=fields.Integer(string='Amarillo')
    porcentajeCian=fields.Integer(string='Cian')
    porcentajeMagenta=fields.Integer(string='Magenta')
    fuente=fields.Selection(selection=[('dcas.dcas', 'DCA'),('helpdesk.ticket', 'Mesa'),('stock.production.lot','Equipo'),('tfs.tfs','Tfs')], default='dcas.dcas')  
    cartuchoNegro=fields.Selection([('a', 'Ninguna serie selecionada')], string='prueba')
    nivelNA=fields.Integer(string='Nivel de toner negro anteior')
    nivelAA=fields.Integer(string='Nivel de toner Amarillo anteior')
    nivelCA=fields.Integer(string='Nivel de toner Cian anteior')
    nivelMA=fields.Integer(string='Nivel de toner Magenta anteior')
    contadorAnteriorCian=fields.Integer(string='contador de ultima solicitud Cian')
    contadorAnteriorAmarillo=fields.Integer(string='contador de ultima solicitud Amarillo')
    contadorAnteriorMagenta=fields.Integer(string='contador de ultima solicitud Magenta')
    contadorAnteriorNegro=fields.Integer(string='contador de ultima solicitud Negro')
    contadorAnteriorColor=fields.Integer(string='contador de ultima solicitud Color')
    paginasProcesadasBN=fields.Integer(string='Páginas procesadas BN')
    paginasProcesadasC=fields.Integer(string='Páginas procesadas Cian')
    paginasProcesadasA=fields.Integer(string='Páginas procesadas Amarillo')
    paginasProcesadasM=fields.Integer(string='Páginas procesadas Magenta')
    x_studio_fecha = fields.Datetime(string='Fecha', default=lambda self: fields.datetime.now())
    #x_studio_fecha = fields.Datetime(string='Fecha')
    renC=fields.Float(string='Rendimiento Cian')
    renA=fields.Float(string='Rendimiento Amarillo')
    renM=fields.Float(string='Rendimiento Magenta')
    renN=fields.Float(string='Rendimiento Negro ')
    
    tablahtml=fields.Text(string='Detalle Equipo')
    comentarioLecturas = fields.Text(string = 'Comentario')
    fechaN=fields.Datetime(string='Fecha de captura')
    fechaA=fields.Datetime(string='Fecha de captura')
    fechaC=fields.Datetime(string='Fecha de captura')
    fechaM=fields.Datetime(string='Fecha de captura')
    tN=fields.Char(string='Ticket BN')
    tA=fields.Char(string='Ticket Amarillo')
    tC=fields.Char(string='Ticket Cian')
    tM=fields.Char(string='Ticket Magenta')
    colorEquipo=fields.Char(string='Color o Bn')
    equipo=fields.Char(string='Equipo')
    ultimaUbicacion=fields.Char(string='Ultima ubicación')
    
    hTicketSerie = fields.Text(string = 'Serie en h.Ticket')
    hTicketCliente = fields.Text(string = 'Cliente')
    hTicketAreaDeAtencion = fields.Text(string = 'Área de atención')
    hTicketUbicacion = fields.Text(string = 'Ubicación')
    hTicketFalla = fields.Text(string = 'Falla')
    hTicketUltimaEtapaTicket = fields.Text(string = 'Última etapa ticket')
    hTicketHojaDeEstado = fields.Text(string = 'Hoja de estado')
    hTicketUltimaNota = fields.Text(string = 'Última nota')
    hTicketFechaNota = fields.Datetime(string = 'Fecha nota')
    hTicketFechaNotaText = fields.Text(string = 'Fecha nota texto')
    ultimaCargaContadoresMesa = fields.Boolean(string = 'Ultima carga al día 22/09/2020')
    esContadorDeTechra = fields.Boolean(string = 'Contador cargado de techra')

    archivoCSV = fields.Binary(string="Archivo a cargar csv")    

    fechaTemporal = fields.Text(string = 'Fecha temporal', store = True)
    
    comentarioDeReinicio = fields.Text(string = 'Comentario de reinicio de contador')
    reinicioDeContador = fields.Boolean(string = 'Reinicio de contador')
    
    ticket_techra = fields.Many2one('helpdesk.ticket.techra', string = 'Ticket techra relacion')
    ticket_techra_texto = fields.Text(string = 'Ticket techra texto')
    creado_por_tickets_techra = fields.Boolean(string = 'Creado por ppanificador de ticket techra', default = False)
    x_studio_tiquete=fields.Many2one('helpdesk.ticket')
    x_numero_serie = fields.Char(string='Numero de serie', store=True)
    x_studio_toner_amarillo=fields.Integer()
    x_studio_toner_cian=fields.Integer()
    x_studio_toner_magenta=fields.Integer()
    x_studio_toner_negro=fields.Integer()
    x_studio_contador_color_anterior=fields.Integer()
    x_studio_contador_mono_anterior=fields.Integer()
    x_studio_contador_mono_anterior_1=fields.Integer()
    x_studio_descripcion = fields.Char(string='Descripción', store=True)
    x_studio_field_no6Rb = fields.Char(string='Fecha mes/año', store=True)
    x_studio_fecha_texto_anio = fields.Char(string='Fecha texto año', store=True)
    x_studio_tickett = fields.Char(string='Ticket Techra', store=True)
    x_studio_fecha_techra = fields.Date(string='Fecha techra', store=True)
    x_studio_robot = fields.Boolean(string='Robot', default=False, store=True)
    x_studio_lectura_anterior_color = fields.Integer(string='Lectura anterior color', store=True)
    x_studio_lectura_anterior_bn = fields.Integer(string='Lectura anterior B/N', store=True)

    
    x_studio_field_qYMJD = fields.Integer(string="Id producto", readonly=True, compute="_compute_x_studio_field_qYMJD")

    @api.depends('serie')
    def _compute_x_studio_field_qYMJD(self):
        self.x_studio_field_qYMJD = 0
        for r in self:
            if r.serie.id and r.serie.product_id.id:
                r['x_studio_field_qYMJD'] = r.serie.product_id.id

    @api.onchange('serie')
    def _get_compatibles_negro(self):
        #domain = [('categ_id', '=', 5), ('x_studio_color', '=', 'Negro'), ('x_studio_toner_compatible.id', '=', self.x_studio_field_qYMJD)]
        domain = [('id', '=', -1)]
        compatibles_list = []
        productos = self.sudo().env['product.product'].search([])
        #productos = productos.sudo().filtered(lambda x:  x.categ_id.id == 5 and x.x_studio_color == 'Negro' and self.x_studio_field_qYMJD in x.x_studio_toner_compatible.ids)
        productos = productos.filtered(lambda x:  x.categ_id.name.lower() == 'toner')
        _logger.info('productos: ' + str(productos.ids))
        for producto in productos:
            compatibles_list.append(producto.id)
        if productos:
            domain = [('id', 'in', compatibles_list)] 
            #return str(domain)
        #return str(domain)
        return {
            'domain': {'x_studio_cartuchonefro': domain}
        }

    x_studio_cartuchonefro = fields.Many2one('product.product', string='Cartucho negro', store=True, )#domain=_get_compatibles_negro

    x_studio_rendimiento_negro = fields.Char(string='Rendimiento Negro', readonly=True, compute="_compute_x_studio_rendimiento_negro")
    @api.depends('x_studio_cartuchonefro')
    def _compute_x_studio_rendimiento_negro(self):
        self.x_studio_rendimiento_negro = ''
        for r in self:
            if r.x_studio_cartuchonefro:
                r['x_studio_rendimiento_negro'] = str(r.x_studio_cartuchonefro.x_studio_rendimiento_toner)

    @api.onchange('serie')
    def _get_compatibles_amarillo(self):
        #domain = [('categ_id', '=', 5), ('x_studio_color', '=', 'Amarillo'), ('x_studio_toner_compatible.id', '=', x_studio_field_qYMJD)]
        domain = [('id', '=', -1)]
        compatibles_list = []
        productos = self.sudo().env['product.product'].search([])
        #productos = productos.sudo().filtered(lambda x:  x.categ_id.id == 5 and x.x_studio_color == 'Amarillo' and self.x_studio_field_qYMJD in x.x_studio_toner_compatible.ids)
        productos = productos.filtered(lambda x:  x.categ_id.name.lower() == 'toner')
        _logger.info('productos: ' + str(productos.ids))
        for producto in productos:
            compatibles_list.append(producto.id)
        if productos:
            domain = [('id', 'in', compatibles_list)] 
            #return str(domain)
        #return str(domain)
        return {
            'domain': {'x_studio_cartucho_amarillo': domain}
        }


    x_studio_cartucho_amarillo = fields.Many2one('product.product', string='Cartucho amarillo', store=True, )#domain=_get_compatibles_amarillo

    x_studio_rendimientoa = fields.Char(string='Rendimiento amarillo', readonly=True, compute="_compute_x_studio_rendimientoa")
    @api.depends('x_studio_cartucho_amarillo')
    def _compute_x_studio_rendimientoa(self):
        self.x_studio_rendimientoa = ''
        for r in self:
            if r.x_studio_cartucho_amarillo:
                r['x_studio_rendimientoa'] = str(r.x_studio_cartucho_amarillo.x_studio_rendimiento_toner)


    @api.onchange('serie')
    def _get_compatibles_cian(self):
        #domain = [('categ_id', '=', 5), ('x_studio_color', '=', 'Cian'), ('x_studio_toner_compatible.id', '=', x_studio_field_qYMJD)]
        domain = [('id', '=', -1)]
        compatibles_list = []
        productos = self.sudo().env['product.product'].search([])
        #productos = productos.sudo().filtered(lambda x:  x.categ_id.id == 5 and x.x_studio_color == 'Cian' and self.x_studio_field_qYMJD in x.x_studio_toner_compatible.ids)
        productos = productos.filtered(lambda x:  x.categ_id.name.lower() == 'toner')
        _logger.info('productos: ' + str(productos.ids))
        for producto in productos:
            compatibles_list.append(producto.id)
        if productos:
            domain = [('id', 'in', compatibles_list)] 
            #return str(domain)
        #return str(domain)
        return {
            'domain': {'x_studio_cartucho_cian_1': domain}
        }

    x_studio_cartucho_cian_1 = fields.Many2one('product.product', string='Cartucho cian', store=True, ) #domain=_get_compatibles_cian

    x_studio_rendimientoc = fields.Char(string='Rendimiento cian', readonly=True, compute="_compute_x_studio_rendimientoc")
    @api.depends('x_studio_cartucho_cian_1')
    def _compute_x_studio_rendimientoc(self):
        self.x_studio_rendimientoc = ''
        for r in self:
            if r.x_studio_cartucho_cian_1:
                r['x_studio_rendimientoc'] = str(r.x_studio_cartucho_cian_1.x_studio_rendimiento_toner)

    @api.onchange('serie')
    def _get_compatibles_magenta(self):
        #domain = [('categ_id', '=', 5), ('x_studio_color', '=', 'Magenta'), ('x_studio_toner_compatible.id', '=', x_studio_field_qYMJD)]
        domain = [('id', '=', -1)]
        compatibles_list = []
        productos = self.sudo().env['product.product'].search([])
        #productos = productos.sudo().filtered(lambda x:  x.categ_id.id == 5 and x.x_studio_color == 'Magenta' and self.x_studio_field_qYMJD in x.x_studio_toner_compatible.ids)
        productos = productos.filtered(lambda x:  x.categ_id.name.lower() == 'toner')
        _logger.info('productos: ' + str(productos.ids))
        for producto in productos:
            compatibles_list.append(producto.id)
        if productos:
            domain = [('id', 'in', compatibles_list)] 
            _logger.info('productos: ' + str(domain))
            #return str(domain)
        #return str(domain)
        return {
            'domain': {'x_studio_cartucho_magenta': domain}
        }


    x_studio_cartucho_magenta = fields.Many2one('product.product', string='Cartucho magenta', store=True, ) #domain=_get_compatibles_magenta

    x_studio_rendimientom = fields.Char(string='Rendimiento magenta', readonly=True, compute="_compute_x_studio_rendimientom")
    @api.depends('x_studio_cartucho_magenta')
    def _compute_x_studio_rendimientom(self):
        self.x_studio_rendimientom = ''
        for r in self:
            if r.x_studio_cartucho_magenta:
                r['x_studio_rendimientom'] = str(r.x_studio_cartucho_magenta.x_studio_rendimiento_toner)








    x_studio_color_o_bn = fields.Char(string='Equipo B/N o Color', readonly=True, compute='_compute_x_studio_color_o_bn')
    @api.depends('serie')
    def _compute_x_studio_color_o_bn(self):
        self.x_studio_color_o_bn = ''
        for r in self:
            if r.serie.id:
                r['x_studio_color_o_bn'] = str(r.serie.x_studio_color_bn)


    @api.onchange('serie')             
    def ultimosContadoresNACM(self):
        #inicializando valores
        self.ultimaUbicacion = ''



      #if self.fuente == 'helpdesk.ticket' or self.fuente == 'tfs.tfs':
        if self.serie.id:
            bn_c = self.sudo().env['stock.production.lot'].search([['id','=',self.serie.id]])
            if bn_c.id and bn_c.x_studio_color_bn:
                self.colorEquipo = bn_c.x_studio_color_bn
            _logger.info("bn_c.x_studio_localidad_2: " + str(bn_c.x_studio_localidad_2))
            if bn_c.id and bn_c.x_studio_localidad_2.id:
                self.ultimaUbicacion = str(bn_c.x_studio_localidad_2.display_name)
            if bn_c.id and bn_c.product_id.id:
                self.equipo = bn_c.product_id.name
            if self.colorEquipo=='B/N':
                n=self.env['dcas.dcas'].search([['serie','=',self.serie.id],['x_studio_toner_negro','=',1],['fuente','=','helpdesk.ticket'],['contadorMono','!=',0]],order='x_studio_fecha desc',limit=1)
            else:
                n=self.env['dcas.dcas'].search([['serie','=',self.serie.id],['x_studio_toner_negro','=',1],['fuente','=','helpdesk.ticket'],['contadorMono','!=',0]],order='x_studio_fecha desc',limit=1)            
            if len(n)>0:
               self.fechaN=n.x_studio_fecha

               if self.colorEquipo=='B/N':
                  self.nivelNA=n.porcentajeNegro
               else:
                  self.nivelNA=n.porcentajeNegro

               self.contadorAnteriorNegro=n.contadorMono
               self.tN=n.x_studio_tickett
            c=self.env['dcas.dcas'].search([['serie','=',self.serie.id],['x_studio_toner_cian','=',1],['fuente','=','helpdesk.ticket']],order='x_studio_fecha desc',limit=1)
            if len(c)>0:
               self.nivelCA=c.porcentajeCian
               self.contadorAnteriorCian=c.contadorColor
               self.fechaC=c.x_studio_fecha
               self.tC=c.x_studio_tickett
            a=self.env['dcas.dcas'].search([['serie','=',self.serie.id],['x_studio_toner_amarillo','=',1],['fuente','=','helpdesk.ticket']],order='x_studio_fecha desc',limit=1)
            if len(a)>0:
               self.nivelAA=a.porcentajeAmarillo
               self.contadorAnteriorAmarillo=a.contadorColor
               self.fechaA=a.x_studio_fecha
               self.tA=a.x_studio_tickett
            m=self.env['dcas.dcas'].search([['serie','=',self.serie.id],['x_studio_toner_magenta','=',1],['fuente','=','helpdesk.ticket']],order='x_studio_fecha desc',limit=1)
            if len(m)>0:
                self.nivelMA=m.porcentajeMagenta
                self.contadorAnteriorMagenta=m.contadorColor
                self.fechaM=m.x_studio_fecha
                self.tM=m.x_studio_tickett
                #select "contadorColor" from dcas_dcas where "porcentajeMagenta"=1 or "porcentajeCian"=1 or "porcentajeNegro"=1  order by x_studio_fecha desc limit 1;
            if self.colorEquipo!='B/N':                
                query="select \"contadorColor\" from dcas_dcas where  serie="+str(self.serie.id)+" and (\"x_studio_toner_amarillo\"=1 or \"x_studio_toner_amarillo\"=1 or \"x_studio_toner_cian\"=1 or \"x_studio_toner_negro\"=1) and \"contadorColor\"!=0 and fuente='helpdesk.ticket' order by x_studio_fecha desc limit 1;"                        
                _logger.info("self inicio id query"+str(query))
                self.env.cr.execute(query)
                informacion = self.env.cr.fetchall()            
                _logger.info("tam"+str(len(informacion)))
                if len(informacion)>0:                   
                   self.contadorAnteriorColor = informacion[0][0]
                else:
                    self.contadorAnteriorColor=0
        if self.serie:
            carn=''
            cara=''
            carc=''
            carm=''
            
            fechan=''
            fechaa=''
            fechac=''
            fecham=''
            
            tn=''
            ta=''
            tc=''
            tm=''
            
            if self.tN:
                tn=self.tN
            if self.tC:
                tc=self.tC
            if self.tA:
                ta=self.tA
            if self.tM:
                tm=self.tM
            
            
            
            if self.fechaN:
                fechan=str((self.fechaN - datetime.timedelta(seconds =6*3600)).strftime('%d-%m-%Y %H:%M:%S'))
            if self.fechaC:
                fechac=str((self.fechaC - datetime.timedelta(seconds =6*3600)).strftime('%d-%m-%Y %H:%M:%S'))
            if self.fechaA:
                fechaa=str((self.fechaA - datetime.timedelta(seconds =6*3600)).strftime('%d-%m-%Y %H:%M:%S'))
            if self.fechaM:
                fecham=str((self.fechaM - datetime.timedelta(seconds =6*3600)).strftime('%d-%m-%Y %H:%M:%S'))
           
            if self.x_studio_cartuchonefro.name:
                carn=str(self.x_studio_cartuchonefro.name)            
            if self.x_studio_cartucho_cian_1.name:
                carc=str(self.x_studio_cartucho_cian_1.name)                
            if self.x_studio_cartucho_amarillo.name:
                cara=str(self.x_studio_cartucho_amarillo.name)                
            if self.x_studio_cartucho_magenta.name:
                carm=str(self.x_studio_cartucho_magenta.name)
                
            style="<html><head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 5px;text-align: left;}</style></head><body>"
            cabecera="<table style='width:100%'><tr><th></th><th>Monocormatico  </th><th> Cian </th><th> Amarillo </th><th> Magenta </th></tr><tr><tr><td></td></tr>"
            ticket='<tr><td> Ticket </td><td>'+tn+'</br>'+'</td> <td>'+tc+' </br> </td> <td>'+' '+ta+'</br> </td> <td>'+tm+'</br> </td> </tr>'
            contadoresActuales='<tr><td> Contadores capturados </td><td>'+str(self.contadorMono)+'</br>'+'</td> <td>'+str(self.contadorColor)+' </br> </td> <td>'+ str(self.contadorColor)+'</br> </td> <td>'+str(self.contadorColor)+' </br> </td> </tr>'
            ultimosContadores='<tr><td> Último Contador </td><td>'+str(self.contadorAnteriorNegro)+'</br>'+'</td> <td>'+str(self.contadorAnteriorCian)+' </br> </td> <td>'+ str(self.contadorAnteriorAmarillo)+'</br> </td> <td>'+str(self.contadorAnteriorMagenta)+' </br> </td> </tr>'
            fechas='<tr><td> Fecha </td><td>'+fechan+'</br>'+'</td> <td>'+fechac+' </br> </td> <td>'+' '+fechaa+'</br> </td> <td>'+fecham+'</br> </td> </tr>'
            paginasProcesadas='<tr><td> Páginas Procesadas </td> <td>'+str(self.paginasProcesadasBN)+'</td> <td>'+str(self.paginasProcesadasC)+'</td> <td>'+ str(self.paginasProcesadasA)+' </td> <td>'+str(self.paginasProcesadasM)+'</td></tr>'        
            rendimientos='<tr><td> Rendimiento </td> <td>'+str(self.renN)+'</td> <td>'+str(self.renC)+'</td> <td>'+ str(self.renA)+' </td> <td>'+str(self.renM)+'</td></tr>'
            niveles='<tr><td> Último nivel </td> <td>'+str(self.nivelNA)+'</td> <td>'+str(self.nivelCA)+'</td> <td>'+ str(self.nivelAA)+' </td> <td>'+str(self.nivelMA)+'</td></tr>'
            nivelesActual='<tr><td> Nivel actual </td> <td>'+str(self.porcentajeNegro)+'</td> <td>'+str(self.porcentajeCian)+'</td> <td>'+ str(self.porcentajeAmarillo)+' </td> <td>'+str(self.porcentajeMagenta)+'</td></tr>'
            cartuchos='<tr><td> Cartuchos Selecionados </td> <td>'+carn+'</td> <td>'+carc+'</td> <td>'+ cara+' </td> <td>'+carm+'</td></tr>'
            cierre="</table></body></html> "
            self.tablahtml=cabecera+ticket+contadoresActuales+ultimosContadores+fechas+paginasProcesadas+rendimientos+niveles+nivelesActual+cartuchos+cierre    
            #query = "update dcas_dcas set tablahtml = \""+cabecera+ticket+ultimosContadores+fechas+paginasProcesadas+rendimientos+niveles+cierre+"\" where id = " + str(self.id) + ";"
            #ss = self.env.cr.execute(query)
    
    @api.onchange('contadorMono')
    def validaMoon(self):        
        contadorM=self.contadorMono
        cam=self.contadorAnteriorNegro                                        
        if cam>contadorM:            
            raise exceptions.ValidationError("Contador Monocromatico Menor")
            
    @api.onchange('contadorMono')
    def validaMoonLectura(self):        
        contadorM=self.contadorMono
        cam=int(self.x_studio_lectura_anterior_bn)                                        
        if cam>contadorM and self.env.user.id!=113:            
            raise exceptions.ValidationError("Contador Monocromatico Menor")

    @api.onchange('contadorColor')
    def validaContadoresLecturas(self):
        contaC=self.contadorColor                       
        cac=int(self.x_studio_lectura_anterior_color)
        if cac>contaC and self.env.user.id!=113:            
            raise exceptions.ValidationError("Contador Color Menor.")       


    @api.onchange('x_studio_cartuchonefro','x_studio_cartucho_amarillo','x_studio_cartucho_cian_1','x_studio_cartucho_magenta', 'contadorMono', 'contadorColor','porcentajeCian','porcentajeNegro','porcentajeMagenta','porcentajeAmarillo')
    def vcalcula(self):
      if self.fuente!='dcas.dcas':
        contaC=self.contadorColor                       
        cac=self.contadorAnteriorColor
        contadorM=self.contadorMono
        if contaC==0:
          self.paginasProcesadasC=0  
        else:    
          self.paginasProcesadasC=contaC-self.contadorAnteriorCian
        if contaC==0:
          self.paginasProcesadasA=0  
        else:    
          self.paginasProcesadasA=contaC-self.contadorAnteriorAmarillo
        if contaC==0:
          self.paginasProcesadasM=0  
        else:    
          self.paginasProcesadasM=contaC-self.contadorAnteriorMagenta
        if contadorM==0:
          self.paginasProcesadasBN=0  
        else:    
          self.paginasProcesadasBN=contadorM-self.contadorAnteriorNegro            
        
        c=self.x_studio_rendimientoc
        a=self.x_studio_rendimientoa
        m=self.x_studio_rendimientom
        n=self.x_studio_rendimiento_negro
        if c == '0':
           c = 1
        if a == '0':
           a = 1
        if m == '0':
           m = 1                        
        if n == '0':
           n = 1                   
        if n:
           self.renN=round(self.paginasProcesadasBN*100/int(n),0)            
        if c:
           self.renC=round(self.paginasProcesadasC*100/int(c),0)
        if a:
           self.renA=round(self.paginasProcesadasA*100/int(a),0)
        if m:
           self.renM=round(self.paginasProcesadasM*100/int(m),0)
        if self.serie:
           carn=''
           cara=''
           carc=''
           carm=''
            
           fechan=''
           fechaa=''
           fechac=''
           fecham=''
            
           tn=''
           ta=''
           tc=''
           tm=''
            
           if self.tN:
              tn=self.tN
           if self.tC:
              tc=self.tC
           if self.tA:
              ta=self.tA
           if self.tM:
              tm=self.tM
            
            
            
           if self.fechaN:
              fechan=str((self.fechaN- datetime.timedelta(seconds =6*3600)).strftime('%d-%m-%Y %H:%M:%S'))
           if self.fechaC:
              fechac=str((self.fechaC- datetime.timedelta(seconds =6*3600)).strftime('%d-%m-%Y %H:%M:%S'))
           if self.fechaA:
              fechaa=str((self.fechaA- datetime.timedelta(seconds =6*3600)).strftime('%d-%m-%Y %H:%M:%S'))
           if self.fechaM:
              fecham=str((self.fechaM- datetime.timedelta(seconds =6*3600)).strftime('%d-%m-%Y %H:%M:%S'))
           
           if self.x_studio_cartuchonefro.name:
              carn=str(self.x_studio_cartuchonefro.name)            
           if self.x_studio_cartucho_cian_1.name:
              carc=str(self.x_studio_cartucho_cian_1.name)                
           if self.x_studio_cartucho_amarillo.name:
              cara=str(self.x_studio_cartucho_amarillo.name)                
           if self.x_studio_cartucho_magenta.name:
              carm=str(self.x_studio_cartucho_magenta.name)
           
           style="<html><head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 5px;text-align: left;}</style></head><body>"
           cabecera="<table style='width:100%'><tr><th></th><th>Monocormatico  </th><th> Cian </th><th> Amarillo </th><th> Magenta </th></tr><tr><tr><td></td></tr>"
           ticket='<tr><td> Ticket </td><td>'+tn+'</br>'+'</td> <td>'+tc+' </br> </td> <td>'+' '+ta+'</br> </td> <td>'+tm+'</br> </td> </tr>'
           ultimosContadores='<tr><td> Último Contador </td><td>'+str(self.contadorAnteriorNegro)+'</br>'+'</td> <td>'+str(self.contadorAnteriorCian)+' </br> </td> <td>'+ str(self.contadorAnteriorAmarillo)+'</br> </td> <td>'+str(self.contadorAnteriorMagenta)+' </br> </td> </tr>'
           contadoresActuales='<tr><td> Contadores capturados </td><td>'+str(self.contadorMono)+'</br>'+'</td> <td>'+str(self.contadorColor)+' </br> </td> <td>'+ str(self.contadorColor)+'</br> </td> <td>'+str(self.contadorColor)+' </br> </td> </tr>'
           fechas='<tr><td> Fecha </td><td>'+fechan+'</br>'+'</td> <td>'+fechac+' </br> </td> <td>'+' '+fechaa+'</br> </td> <td>'+fecham+'</br> </td> </tr>'
           paginasProcesadas='<tr><td> Páginas Procesadas </td> <td>'+str(self.paginasProcesadasBN)+'</td> <td>'+str(self.paginasProcesadasC)+'</td> <td>'+ str(self.paginasProcesadasA)+' </td> <td>'+str(self.paginasProcesadasM)+'</td></tr>'        
           rendimientos='<tr><td> Rendimiento </td> <td>'+str(self.renN)+'%</td> <td>'+str(self.renC)+'%</td> <td>'+ str(self.renA)+'% </td> <td>'+str(self.renM)+'%</td></tr>'
           niveles='<tr><td> Último nivel </td> <td>'+str(self.nivelNA)+'</td> <td>'+str(self.nivelCA)+'</td> <td>'+ str(self.nivelAA)+' </td> <td>'+str(self.nivelMA)+'</td></tr>'
           nivelesActual='<tr><td> Nivel actual </td> <td>'+str(self.porcentajeNegro)+'</td> <td>'+str(self.porcentajeCian)+'</td> <td>'+ str(self.porcentajeAmarillo)+' </td> <td>'+str(self.porcentajeMagenta)+'</td></tr>'
           cartuchos='<tr><td> Cartuchos Selecionados </td> <td>'+carn+'</td> <td>'+carc+'</td> <td>'+ cara+' </td> <td>'+carm+'</td></tr>'
           cierre="</table></body></html> "
           self.tablahtml=cabecera+ticket+contadoresActuales+ultimosContadores+fechas+paginasProcesadas+rendimientos+niveles+nivelesActual+cartuchos+cierre     
        
           """ 
           style="<html><head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 5px;text-align: left;}</style></head><body>"
           cabecera="<table style='width:100%'><tr><th></th><th>Monocormatico  </th><th> Cian </th><th> Amarillo </th><th> Magenta </th></tr><tr><tr><td></td></tr>"
           ticket='<tr><td> Ticket </td><td>'+str(self.tN)+'</br>'+'</td> <td>'+str(self.tC)+' </br> </td> <td>'+' '+str(self.tA)+'</br> </td> <td>'+str(self.tM)+'</br> </td> </tr>'
           ultimosContadores='<tr><td> Último Contador </td><td>'+str(self.contadorAnteriorNegro)+'</br>'+'</td> <td>'+str(self.contadorAnteriorCian)+' </br> </td> <td>'+ str(self.contadorAnteriorAmarillo)+'</br> </td> <td>'+str(self.contadorAnteriorMagenta)+' </br> </td> </tr>'
           fechas='<tr><td> Fecha </td><td>'+str(self.fechaN)+'</br>'+'</td> <td>'+str(self.fechaC)+' </br> </td> <td>'+' '+str(self.fechaA)+'</br> </td> <td>'+str(self.fechaM)+'</br> </td> </tr>'
           paginasProcesadas='<tr><td> Páginas Procesadas </td> <td>'+str(self.paginasProcesadasBN)+'</td> <td>'+str(self.paginasProcesadasC)+'</td> <td>'+ str(self.paginasProcesadasA)+' </td> <td>'+str(self.paginasProcesadasM)+'</td></tr>'        
           rendimientos='<tr><td> Rendimiento </td> <td>'+str(self.renN)+'</td> <td>'+str(self.renC)+'</td> <td>'+ str(self.renA)+' </td> <td>'+str(self.renM)+'</td></tr>'
           niveles='<tr><td> Último nivel </td> <td>'+str(self.nivelNA)+'</td> <td>'+str(self.nivelCA)+'</td> <td>'+ str(self.nivelAA)+' </td> <td>'+str(self.nivelMA)+'</td></tr>'
           cartuchos='<tr><td> Cartuchos Selecionados </td> <td>'+str(self.x_studio_cartuchonefro.name)+'</td> <td>'+str(self.x_studio_cartucho_cian_1.name)+'</td> <td>'+ str(self.x_studio_cartucho_amarillo.name)+' </td> <td>'+str(self.x_studio_cartucho_magenta.name)+'</td></tr>'
           cierre="</table></body></html> "
           self.tablahtml=cabecera+ticket+ultimosContadores+fechas+paginasProcesadas+rendimientos+niveles+cartuchos+cierre
           """
        
                    
                
            
    @api.onchange('contadorColor')
    def validaContadores(self):
        contaC=self.contadorColor                       
        cac=self.contadorAnteriorColor
        contadorM=self.contadorMono
        if cac>contaC:            
            raise exceptions.ValidationError("Contador Color Menor.")
            
    
    """
    @api.onchange('contadorColor','contadorMono','x_studio_cartuchonefro','x_studio_cartucho_amarillo','x_studio_cartucho_cian_1','x_studio_cartucho_magenta')
    def table(self):
        if self.serie:
            style="<html><head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 5px;text-align: left;}</style></head><body>"
            cabecera="<table style='width:100%'><caption>Info xD</caption><tr><th></th><th>Monocormatico  </th><th> Cian </th><th> Amarillo </th><th> Magenta </th></tr><tr><tr><td></td></tr>"
            ticket='<tr><td> Ticket </td><td>'+str(self.tN)+'</br>'+'</td> <td>'+str(self.tC)+' </br> </td> <td>'+' '+str(self.tA)+'</br> </td> <td>'+str(self.tM)+'</br> </td> </tr>'
            ultimosContadores='<tr><td> Último Contador </td><td>'+str(self.contadorAnteriorNegro)+'</br>'+'</td> <td>'+str(self.contadorAnteriorCian)+' </br> </td> <td>'+ str(self.contadorAnteriorAmarillo)+'</br> </td> <td>'+str(self.contadorAnteriorMagenta)+' </br> </td> </tr>'
            fechas='<tr><td> Fecha </td><td>'+str(self.fechaN)+'</br>'+'</td> <td>'+str(self.fechaC)+' </br> </td> <td>'+' '+str(self.fechaA)+'</br> </td> <td>'+str(self.fechaM)+'</br> </td> </tr>'
            paginasProcesadas='<tr><td> Páginas Procesadas </td> <td>'+str(self.paginasProcesadasBN)+'</td> <td>'+str(self.paginasProcesadasC)+'</td> <td>'+ str(self.paginasProcesadasA)+' </td> <td>'+str(self.paginasProcesadasM)+'</td></tr>'        
            rendimientos='<tr><td> Rendimiento </td> <td>'+str(self.renN)+'</td> <td>'+str(self.renC)+'</td> <td>'+ str(self.renA)+' </td> <td>'+str(self.renM)+'</td></tr>'
            niveles='<tr><td> Último nivel </td> <td>'+str(self.nivelNA)+'</td> <td>'+str(self.nivelCA)+'</td> <td>'+ str(self.nivelAA)+' </td> <td>'+str(self.nivelMA)+'</td></tr>'
            cierre="</table></body></html> "
            self.tablahtml=cabecera+ticket+ultimosContadores+fechas+paginasProcesadas+rendimientos+niveles+cierre                                                                                                                                                                                 
    """

    
    def editar_contadores_wizard(self):
        wiz = self.env['contadores.dca.editar.contadores'].create({'dca_id': self.id})
        #wiz.productos = [(6, 0, self.x_studio_productos.ids)]
        view = self.env.ref('contadores.view_dca_editar_contadores')
        return {
            'name': _('Editar contadores'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'contadores.dca.editar.contadores',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': wiz.id,
            'context': self.env.context,
        }
    
    
    def reiniciar_contadores_wizard(self):
        wiz = self.env['contadores.dca.reiniciar.contadores'].create({'dca_id': self.id})
        #wiz.productos = [(6, 0, self.x_studio_productos.ids)]
        view = self.env.ref('contadores.view_dca_reiniciar_contadores')
        return {
            'name': _('Reiniciar contadores'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'contadores.dca.reiniciar.contadores',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': wiz.id,
            'context': self.env.context,
        }

    


class contadoresexcel(models.Model):
    _name = 'contadores.excel'    
    _description = 'Contadores carga excel'
    name = fields.Char()
    mes=fields.Selection(valores,string='Mes')
    anio= fields.Selection(get_years(), string='Año')
    csv = fields.Binary(string="CSV")
    detallecsv =  fields.One2many('contadores.contadores.detalle', 'contadoresexcel', string='Contadores por csv ')
    
class contadores(models.Model):
    _name = 'contadores.contadores'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Contadores Cliente'
    name = fields.Char()
    
    mes=fields.Selection(valores,string='Mes',default='04')
    anio= fields.Selection(get_years(), string='Año',default=2020)
    archivoglobal = fields.Many2many('ir.attachment',string="Evidencia global")    
    

    excelD = fields.Binary(string="Documento Excel")      
    dca = fields.One2many('dcas.dcas',inverse_name='contador_id',string='DCAS')
    cliente = fields.Many2one('res.partner', store=True,string='Cliente')
    localidad=fields.Many2one('res.partner',store='True',string='Localidad')
    archivo=fields.Binary(store='True',string='Archivo')
    estado=fields.Selection(selection=[('Abierto', 'Abierto'),('Incompleto', 'Incompleto'),('Valido','Valido')],widget="statusbar", default='Abierto')  
    dom=fields.Char(readonly="1",invisible="1")
    order_line = fields.One2many('contadores.lines','ticket',string='Order Lines')
    csvD = fields.Binary(string="Cargar por DCA csv")
    prefacturas=fields.Text(string="Pre-Factura")
    
    
    detalle = fields.One2many('contadores.contadores.detalle', inverse_name='contadores', string='Contadores', store=True)

    x_studio_estado_capturas = fields.Char(string="Estado Capturas:", readonly=True, compute="_compute_x_studio_estado_capturas")

    x_studio_contratos = fields.Many2many('contrato', string='Contrato')

    x_studio_facturas = fields.Many2many('account.move',string="Facturas")    

    @api.depends('detalle')
    def _compute_x_studio_estado_capturas(self):
        self.x_studio_estado_capturas = ''
        for r in self:
            a=len(r.dca)
            t=True
            if a>0:
              for d in r.dca:
                  h=d.x_studio_capturar
                  if str(h)=='False':
                     t=False
              if t:
                 r['x_studio_estado_capturas']='Listo'
              else:
                 r['x_studio_estado_capturas']='No listo'
    
    
    @api.onchange('cliente')
    def dameclientes(self):        
        if self.cliente:
           self.x_studio_contratos=[(6, 0, [])]
           s=self.env['contrato'].search([['cliente','=',self.cliente.id]])        
           self.x_studio_contratos=s.ids           

    
    def selecionaTODOContratos(self):        
        if len(self.x_studio_contratos)>0:
            for r in self.x_studio_contratos:
                r.x_studio_cobrar_contrato=True
                      
    def desSelecionaTODOContratos(self):        
        if len(self.x_studio_contratos)>0:
            for r in self.x_studio_contratos:
                r.x_studio_cobrar_contrato=False      

    
    def selecionaTODOLecturas(self):        
        if len(self.dca)>0:
            for r in self.dca:
                r.x_studio_capturar=True
                      
    def desSelecionaTODOLecturas(self):        
        if len(self.dca)>0:
            for r in self.dca:
                r.x_studio_capturar=False      
    

    
    #@api.onchange('serie_aux')
    def getid(self):
        self.serie=self.env['stock.production.lot'].search([['name','=',self.serie_aux]]).id
        
    
    
    def carga_contadores_fac(self):
        if self.x_studio_estado_capturas=='Listo':
            """
            for r in self.detalle:
                if r.desc!='capturado':
                   rr=self.env['dcas.dcas'].create({'serie': r.producto
                                                 ,'contadorColor':r.ultimaLecturaColor
                                                 ,'contadorMono':r.ultimaLecturaBN
                                                 ,'fuente':'dcas.dcas'
                                                 ,'x_studio_field_no6Rb':str(self.anio)+'-'+str(self.mes)
                                                 ,'x_studio_fecha_texto_anio':str(valores[int(self.mes[1])-1][1])+' de '+str(self.anio)
                                                })
            """                                                
            #ff=self.env['contrato'].search([('cliente', '=',self.cliente.id)])
            prefacturas=''
            id=0
            for rs in self.x_studio_contratos:
                rz=str(self.cliente.razonSocial)
                if rz=='0':                  
                  id=3                  
                if rz=='1':                  
                  id=1                  
                if rz=='2':                  
                  id=4                  
                if rz=='3':                    
                  id=2
                if rs.x_studio_cobrar_contrato:
                    a=self.env['sale.order'].create({'partner_id':self.cliente.id,'x_studio_factura':'si','month':self.mes,'year':self.anio,'company_id':id})
                    self.env.cr.execute("insert into x_contrato_sale_order_rel (sale_order_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")    
                    #https://gnsys-corp.odoo.com/web?#id=2477&action=1167&model=sale.order&view_type=form&menu_id=406
                    prefacturas="<a href='https://gnsys-corp.odoo.com/web?#id="+str(a.id)+"&action=1167&model=sale.order&view_type=form&menu_id=406' target='_blank'>"+str(a.name)+"</a>"+' '+prefacturas                
                    ss=self.env['servicios'].search([('contrato', '=',rs.id)])
                    for sg in ss:                                        
                        if sg.nombreAnte=='SERVICIO DE PCOUNTER' or sg.nombreAnte=='SERVICIO DE PCOUNTER1' or sg.nombreAnte=='ADMINISTRACION DE DOCUMENTOS CON PCOUNTER' or sg.nombreAnte=='SERVICIO DE MANTENIMIENTO DE PCOUNTER' or sg.nombreAnte=='SERVICIO DE MANTENIMIENTO PCOUNTER' or sg.nombreAnte=='RENTA DE LICENCIAMIENTO PCOUNTER':           
                            self.env.cr.execute("insert into x_sale_order_servicios_rel (sale_order_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='SERVICIO DE TFS' or sg.nombreAnte=='OPERADOR TFS' or sg.nombreAnte=='TFS' or sg.nombreAnte=='SERVICIO DE TFS ' :                        
                            self.env.cr.execute("insert into x_sale_order_servicios_rel (sale_order_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='SERVICIO DE MANTENIMIENTO':                        
                            self.env.cr.execute("insert into x_sale_order_servicios_rel (sale_order_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='SOPORTE Y MANTENIMIENTO DE EQUIPOS':
                            self.env.cr.execute("insert into x_sale_order_servicios_rel (sale_order_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='SERVICIO DE ADMINISTRADOR KM NET MANAGER':                        
                            self.env.cr.execute("insert into x_sale_order_servicios_rel (sale_order_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='PAGINAS IMPRESAS EN BN':                        
                            self.env.cr.execute("insert into x_sale_order_servicios_rel (sale_order_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='PAPEL 350,000 HOJAS':                        
                            self.env.cr.execute("insert into x_sale_order_servicios_rel (sale_order_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='LECTORES DE PROXIMIDAD':                        
                            self.env.cr.execute("insert into x_sale_order_servicios_rel (sale_order_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")        
                        if sg.nombreAnte=='RENTA MENSUAL DE LICENCIA  7 EMBEDED' or sg.nombreAnte=='RENTA MENSUAL DE LICENCIA  14 EMBEDED' or  sg.nombreAnte=='RENTA MENSUAL DE LICENCIA  2 EMBEDED':                        
                            self.env.cr.execute("insert into x_sale_order_servicios_rel (sale_order_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                                 
            self.prefacturas=prefacturas    
    
    
    def carga_contadores_fac_invo(self):
        #if self.x_studio_estado_capturas=='Listo':
            _logger.info('paso 566')
            prefacturas=''
            id=0
            for rs in self.x_studio_contratos:
                _logger.info('paso 570')
                rz=str(self.cliente.razonSocial)
                dias=rs.diasCredito
                metodoPago=rs.metodPago
                formaPago=rs.formaDePago
                uso=rs.usoCFDI
                plazo=0
                usoF=''
                diario=0                                
                mes=dict(self._fields['mes'].selection).get(self.mes)
                anio=self.anio                                                                
                if uso:
                  usoF=dict(rs._fields['usoCFDI'].selection).get(uso).split(' ')[0]  
                
                
                if rz=='0':                  
                  id=3
                  diario=33
                if rz=='1':                  
                  id=1    
                  diario=1
                if rz=='2':                  
                  id=4     
                  diario=53 
                if rz=='3':                    
                  id=2
                  diario=43
                
                if dias==30:
                  plazo=4 
                if dias==45:
                  plazo=10
                if dias==60:
                  plazo=11
                if dias==90:
                  plazo=12
                
                
                if rs.x_studio_cobrar_contrato :

                    if metodoPago==6 and dias <30:
                      raise exceptions.ValidationError("faltan método de pago incorrecto o días de crédico incorrecto")
                    if metodoPago==5:
                        plazo=1

                    if not metodoPago:
                      raise exceptions.ValidationError("faltan método de pago."+metodoPago)


                    if not self.cliente.vat or not len(str(self.cliente.vat))>11:
                      raise exceptions.ValidationError("falta rfc para crear factura valor :"+str(fact.partner_id.vat))

                    if not uso:
                      raise exceptions.ValidationError("faltan usocfdi para crear factura "+str(uso))

                    if not formaPago :
                      raise exceptions.ValidationError("faltan forma de pago para crear factura ."+str(formaPago))                    
                    _logger.info('paso 627 a')
                    prefacturas=''
                    #a= self.env['account.move'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'periodo':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                    a= self.env['account.move'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'company_id':1,'journal_id':1,'move_type':'out_invoice'}) 
                    self.env.cr.execute("insert into x_account_move_contrato_rel (account_move_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                    #https://gnsys-corp-stam-1742347.dev.odoo.com/web#id=str(a.id)&action=325&active_id=1&model=account.invoice&view_type=form&menu_id=370
                    #prefacturas="<a href='https://gnsys-corp-stam-1742347.dev.odoo.com/web#id="+str(a.id)+"&action=325&active_id=1&model=account.invoice&view_type=form&menu_id=370' target='_blank'>"+str(a.id)+"</a>"+' '+prefacturas                
                    ss=self.env['servicios'].search([('contrato', '=',rs.id)])                    
                    for sg in ss:                                        
                        if sg.nombreAnte=='SERVICIO DE PCOUNTER' or sg.nombreAnte=='SERVICIO DE PCOUNTER1' or sg.nombreAnte=='ADMINISTRACION DE DOCUMENTOS CON PCOUNTER' or sg.nombreAnte=='SERVICIO DE MANTENIMIENTO DE PCOUNTER' or sg.nombreAnte=='SERVICIO DE MANTENIMIENTO PCOUNTER' or sg.nombreAnte=='RENTA DE LICENCIAMIENTO PCOUNTER':           
                            self.env.cr.execute("insert into x_account_move_servicios_rel (account_move_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='SERVICIO DE TFS' or sg.nombreAnte=='OPERADOR TFS' or sg.nombreAnte=='TFS' or sg.nombreAnte=='SERVICIO DE TFS ' :                        
                            self.env.cr.execute("insert into x_account_move_servicios_rel (account_move_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='SERVICIO DE MANTENIMIENTO':                        
                            self.env.cr.execute("insert into x_account_move_servicios_rel (account_move_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='SOPORTE Y MANTENIMIENTO DE EQUIPOS':
                            self.env.cr.execute("insert into x_account_move_servicios_rel (account_move_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='SERVICIO DE ADMINISTRADOR KM NET MANAGER':                        
                            self.env.cr.execute("insert into x_account_move_servicios_rel (account_move_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='PAGINAS IMPRESAS EN BN':                        
                            self.env.cr.execute("insert into x_account_move_servicios_rel (account_move_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='PAPEL 350,000 HOJAS':                        
                            self.env.cr.execute("insert into x_account_move_servicios_rel (account_move_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='LECTORES DE PROXIMIDAD':                        
                            self.env.cr.execute("insert into x_account_move_servicios_rel (account_move_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")        
                        if sg.nombreAnte=='RENTA MENSUAL DE LICENCIA  7 EMBEDED' or sg.nombreAnte=='RENTA MENSUAL DE LICENCIA  14 EMBEDED' or  sg.nombreAnte=='RENTA MENSUAL DE LICENCIA  2 EMBEDED':
                            self.env.cr.execute("insert into x_account_move_servicios_rel (account_move_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")        
                    a.llamado_boton_factu()
                
                if rs.x_studio_cobrar_contrato and (rs.dividirServicios or rs.dividirLocalidades or rs.dividirExcedentes):
                    _logger.info('tiempo 11 : paso')
                    a.llamado_boton_factu()
                    _logger.info('tiempo 11 : no paso')
                    
                    
                    """
                    #raise exceptions.ValidationError("Aquie entro  ." )               
                    ss=self.env['servicios'].search([('contrato', '=',rs.id)])
                    
                    for sg in ss:                                        
                        if sg.nombreAnte=='SERVICIO DE PCOUNTER' or sg.nombreAnte=='SERVICIO DE PCOUNTER1' or sg.nombreAnte=='ADMINISTRACION DE DOCUMENTOS CON PCOUNTER' or sg.nombreAnte=='SERVICIO DE MANTENIMIENTO DE PCOUNTER' or sg.nombreAnte=='SERVICIO DE MANTENIMIENTO PCOUNTER' or sg.nombreAnte=='RENTA DE LICENCIAMIENTO PCOUNTER':           
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='SERVICIO DE TFS' or sg.nombreAnte=='OPERADOR TFS' or sg.nombreAnte=='TFS' or sg.nombreAnte=='SERVICIO DE TFS ' :                        
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")
                            
                        if sg.nombreAnte=='SERVICIO DE MANTENIMIENTO':                        
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                            
                        if sg.nombreAnte=='SOPORTE Y MANTENIMIENTO DE EQUIPOS':
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='SERVICIO DE ADMINISTRADOR KM NET MANAGER':                        
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                    
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='PAGINAS IMPRESAS EN BN':                        
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='PAPEL 350,000 HOJAS':                        
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='LECTORES DE PROXIMIDAD':                        
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")        
                        if sg.nombreAnte=='RENTA MENSUAL DE LICENCIA  7 EMBEDED' or sg.nombreAnte=='RENTA MENSUAL DE LICENCIA  14 EMBEDED' or  sg.nombreAnte=='RENTA MENSUAL DE LICENCIA  2 EMBEDED':  
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='Costo por página procesada BN o color':  #desde aqui
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='Renta base + costo de página procesada BN o color':  
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='Renta base con ML incluidas BN o color + ML. excedentes' or sg.nombreAnte=='Renta base con páginas incluidas BN o color + pag. excedentes':  
                            #raise exceptions.ValidationError("Aquie entro  ." +str(ss) )               
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")    
                        if sg.nombreAnte=='Renta global con páginas incluidas BN o color + pag. Excedentes':  
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")        
                        if sg.nombreAnte=='Renta global + costo de página procesada BN o color':  
                            a=self.env['account.invoice'].create({'x_studio_captura':self.id,'partner_id':self.cliente.id,'month':self.mes,'year':self.anio,'x_studio_periodo_1':mes +' de '+str(anio) ,'company_id':id,'l10n_mx_edi_payment_method_id':formaPago,'payment_term_id':plazo,'l10n_mx_edi_usage':usoF,'journal_id':diario})
                            self.env.cr.execute("insert into x_account_invoice_contrato_rel (account_invoice_id, contrato_id) values (" +str(a.id) + ", " +  str(rs.id) + ");")                        
                            self.env.cr.execute("insert into x_account_invoice_servicios_rel (account_invoice_id, servicios_id) values (" +str(a.id) + ", " +  str(sg.id) + ");")            
                    """#a.llamado_boton_factu()         
                
                    
                    
                    
                    #raise exceptions.ValidationError("vamos a dividir xD")                    
                    
                    
            
            
            
            
            
            #self.env['sale.order'].llamado_boton()
            self.prefacturas=prefacturas         
            
    
    
    def genera_excel(self):
        workbook = xlsxwriter.Workbook('Example2.xlsx')                        
        for contrato in self.x_studio_contratos:
            if contrato.x_studio_cobrar_contrato:
                worksheet = workbook.add_worksheet(str(contrato.idTechraRef))                
                neg = workbook.add_format({'border': 2})

                # Start from the first cell. 
                # Rows and columns are zero indexed. 
                row = 0
                column = 0
                perido=str(self.anio)+'-'+str(self.mes)
                periodoAnterior=''
                mesaA=''
                mesaAA=''
                anioA=''
                mes=''
                #mesA=''
                #anioA=''
                i=0
                for f in valores:                
                    if f[0]==str(self.mes):                
                        mesaA=str(valores[i-1][0])
                    i=i+1
                anios=get_years()
                i=0
                if str(self.mes)=='01':
                   anioA=str(int(self.anio)-1)
                else:    
                   anioA=str(self.anio)              
                periodoAnterior= anioA+'-'+mesaA 


                if mesaA =='01':
                   masaAA="ENERO"
                if mesaA =='02':
                   masaAA="FEBRERO"
                if mesaA =='03':
                   masaAA="MARZO"
                if mesaA =='04':
                   masaAA="ABRIL"
                if mesaA =='05':
                   masaAA="MAYO"
                if mesaA =='06':
                   masaAA="JUNIO"
                if mesaA =='07':
                   masaAA="JULIO"
                if mesaA =='08':
                   masaAA="AGOSTO"
                if mesaA =='09':
                   masaAA="SEPTIEMBRE"
                   #raise exceptions.ValidationError("Contador Color Menor. "+masaAA+" dentro "+mesaA)
                if mesaA =='10':
                   masaAA="OCTUBRE"
                if mesaA =='11':
                   masaAA="NOVIEMBRE"
                if mesaA =='12':
                   masaAA="DICIEMBRE"

                
                if str(self.mes)=='01':
                   mes="ENERO"
                if str(self.mes)=='02':
                   mes="FEBRERO"
                if str(self.mes)=='03':
                   mes="MARZO"
                if str(self.mes)=='04':
                   mes="ABRIL"
                if str(self.mes)=='05':
                   mes="MAYO"
                if str(self.mes)=='06':
                   mes="JUNIO"
                if str(self.mes)=='07':
                   mes="JULIO"
                if str(self.mes)=='08':
                   mes="AGOSTO"
                if str(self.mes)=='09':
                   mes="SEPTIEMBRE"
                if str(self.mes)=='10':
                   mes="OCTUBRE"
                if str(self.mes)=='11':
                   mes="NOVIEMBRE"
                if str(self.mes)=='12':
                   mes="DICIEMBRE"
                content = ["No.", "Localidad", "Modelo", "No. Serie","B/N ["+masaAA+"]", "Color ["+masaAA+"]","B/N ["+mes+"]", "Color ["+mes+"]", "Impresiones B/N", "Impresiones Color","Excedentes B&N","Excedentes Color","Subtotal","IVA","Total","Ubicación","Comentario"]                         
                #content = ["No.", "Localidad", "Modelo", "No. Serie","B/N ["+str(valores[int(mesaA)-1][1])+"]", "Color ["+str(valores[int(mesaA)-1][1])+"]","B/N ["+str(valores[int(self.mes[1])-1][1])+"]", "Color ["+str(valores[int(self.mes[1])-1][1])+"]", "Impresiones B/N", "Impresiones Color","Excedentes B&N","Excedentes Color","Subtotal","IVA","Total","Ubicación","Comentario"]        
                #abajo 0 derecha 0
                bold = workbook.add_format({'bold': True})
                if self.cliente:
                   worksheet.write(0, 0, "CLIENTE: "+str(self.cliente.name),bold)
                   dir=self.serie=self.env['res.partner'].search([['parent_id','=',self.cliente.id],["type","=","invoice"]],order='create_date desc',limit=1)        
                   if dir.street_name:
                      worksheet.write(1, 0, str(dir.street_name))
                   if dir.name:     
                      worksheet.write(2, 0, "CONTACTO: "+str(dir.name))
                   if dir.phone:
                      worksheet.write(3, 1, str(dir.phone))
                   if dir.email:     
                      worksheet.write(4, 1, str(dir.email))




                #falta costo y renta global y cosot por click bn 
                i=0
                for item in content :           
                    worksheet.write(5, i, item,neg)            
                    row += 1
                    i=i+1
                i=6
                worksheet.set_column('B:B', 40)
                #worksheet.set_column(2, 2, 40)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 30)
                worksheet.set_column('E:E', 30)
                worksheet.set_column('F:F', 30)
                worksheet.set_column('G:G', 30)
                worksheet.set_column('H:H', 30)

                worksheet.autofilter('A6:Q6')

                #worksheet.insert_image('O2', 'gnsys.png')
                if len(self.dca)>0: 
                    ser=self.serie=self.env['servicios'].search([['id','=',self.dca[0].x_studio_servicio]])
                else:
                    raise exceptions.ValidationError("Nada que generar ")
                rgl=0
                tbn=0
                tc=0
                tsubt=0
                tiva=0
                total=0
                re=self.env['servicios'].search([['contrato','=',contrato.id]])
                g=6
                totalsr=0
                ivatt=0
                ttotal=0
                eebn=0
                eec=0
                ebnx=0
                resto=0
                restoc=0
                for rd in re:
                    if rd.nombreAnte=='Renta global con páginas incluidas BN o color + pag. Excedentes' :                    
                       eec=0
                       eebn=0  
                       for rpt in self.dca :                                
                           if int(rpt.x_studio_servicio)==rd.id :                       
                                worksheet.write(i, 0, rpt.x_studio_indice,neg)
                                worksheet.write(i, 1, rpt.x_studio_locacin,neg)
                                worksheet.write(i, 2, rpt.x_studio_modelo,neg)
                                worksheet.write(i, 3, rpt.serie.name,neg)            
                                worksheet.write(i, 4, rpt.x_studio_lectura_anterior_bn,neg)
                                worksheet.write(i, 5, rpt.x_studio_lectura_anterior_color,neg)                        
                                worksheet.write(i, 6, rpt.contadorMono,neg)
                                worksheet.write(i, 7, rpt.contadorColor,neg)   
                                if rpt.contadorMono==0:
                                   ebn=0
                                else:
                                   ebn=rpt.contadorMono-rpt.x_studio_lectura_anterior_bn
                                if rpt.contadorColor==0:
                                   ec=0
                                else:                
                                   ec=rpt.contadorColor-rpt.x_studio_lectura_anterior_color                    
                                worksheet.write(i, 15, rpt.x_studio_ubicacin,neg)                                                            
                                worksheet.write(i, 16, rpt.comentarioLecturas,neg)                                                            
                                worksheet.write(i, 8, ebn,neg)
                                worksheet.write(i, 9, ec,neg)

                                if rpt.x_studio_color_o_bn=='B/N':                                                         
                                   eebn=ebn+eebn
                                if rpt.x_studio_color_o_bn=='Color':                                                         
                                   eebn=ebn+eebn                                                                                   
                                   eec=ec+eec

                                i=i+1
                       if eebn>rd.bolsaBN:
                           resto=eebn-rd.bolsaBN
                           totalsr=resto*rd.clickExcedenteBN+totalsr
                           ivatt=round(resto*rd.clickExcedenteBN*.16,2)+ivatt
                           ttotal=round(resto*rd.clickExcedenteBN*.16,2) +resto*rd.clickExcedenteBN+ttotal
                       if eec>rd.bolsaColor:
                           restoc=eec-rd.bolsaColor
                           totalsr=restoc*rd.clickExcedenteColor+totalsr
                           ivatt=round(restoc*rd.clickExcedenteColor*.16,2)+ivatt
                           ttotal=round(restoc*rd.clickExcedenteColor*.16,2)+restoc*rd.clickExcedenteColor+ttotal                            

                       totalsr=float(rd.rentaMensual)+totalsr
                       ivatt=round(float(rd.rentaMensual)*.16,2)+ivatt
                       ttotal=round(float(rd.rentaMensual)*.16,2) + float(rd.rentaMensual) + ttotal
                    if rd.nombreAnte=='Renta global + costo de página procesada BN o color' and len(re)>0:
                       rb=0 
                       for rpt in self.dca :
                           if int(rpt.x_studio_servicio)==rd.id :                        
                                worksheet.write(i, 0, rpt.x_studio_indice,neg)
                                worksheet.write(i, 1, rpt.x_studio_locacin,neg)
                                worksheet.write(i, 2, rpt.x_studio_modelo,neg)
                                worksheet.write(i, 3, rpt.serie.name,neg)           
                                worksheet.write(i, 4, rpt.x_studio_lectura_anterior_bn,neg)
                                worksheet.write(i, 5, rpt.x_studio_lectura_anterior_color,neg)                        
                                worksheet.write(i, 6, rpt.contadorMono,neg)
                                worksheet.write(i, 7, rpt.contadorColor,neg)
                                if str(rpt.serie.x_studio_estado)!='Back-up':   
                                    if rpt.contadorMono==0:
                                       ebn=0
                                    else:
                                       ebn=rpt.contadorMono-rpt.x_studio_lectura_anterior_bn
                                    if rpt.contadorColor==0:
                                       ec=0
                                    else:                
                                       ec=rpt.contadorColor-rpt.x_studio_lectura_anterior_color                    
                                    worksheet.write(i, 15, rpt.x_studio_ubicacin,neg)
                                    #worksheet.write(i, 16, len(rd))
                                    worksheet.write(i, 16, rpt.comentarioLecturas,neg)                                                            
                                    worksheet.write(i, 8, ebn,neg)
                                    worksheet.write(i, 9, ec,neg)                        
                                    if rpt.x_studio_color_o_bn=='B/N':                                    
                                       bs= (ebn*rd.clickExcedenteBN)
                                       #eebn=ebn+eebn
                                       worksheet.write(i, 12, bs,neg)
                                       iva=round(bs*.16,2)
                                       ivatt=iva+ivatt
                                       worksheet.write(i, 13,'$ '+str(iva),neg )
                                       worksheet.write(i, 14,'$ '+str(iva +bs) ,neg)
                                       totalsr=bs+totalsr
                                       ttotal=(iva +bs)+ttotal                        
                                    if rpt.x_studio_color_o_bn=='Color':
                                       bsc=(ec*rd.clickExcedenteColor)+(ebn*rd.clickExcedenteBN)
                                       #eec=ec+eec
                                       worksheet.write(i, 12, bsc,neg) 
                                       iva=round(bsc*.16,2)
                                       ivatt=iva+ivatt
                                       worksheet.write(i, 13,'$ '+str(iva) ,neg) 
                                       worksheet.write(i, 14,'$ '+str(iva +bsc) ,neg)
                                       totalsr=bsc+totalsr
                                       ttotal=(iva +bsc)+ttotal                            
                                    if rpt.x_studio_color_o_bn=='B/N':                                                         
                                       eebn=ebn+eebn
                                    if rpt.x_studio_color_o_bn=='Color':                                                         
                                       eebn=ebn+eebn                                                                                   
                                       eec=ec+eec                           
                                    i=i+1                        
                                    if rb==0:     
                                      totalsr=float(rd.rentaMensual)+totalsr
                                      ivatt=round(float(rd.rentaMensual)*.16,2)+ivatt
                                      ttotal=round(float(rd.rentaMensual)*.16,2) +float(rd.rentaMensual)+ttotal
                                    rb=rb+1
                           #que se cobre solo una vez y no n veces
                for rd in re:
                    for rpt in self.dca :
                        if int(rpt.x_studio_servicio)==rd.id :                                        
                            if rpt.contadorMono==0:
                               ebn=0
                            else:
                               ebn=rpt.contadorMono-rpt.x_studio_lectura_anterior_bn
                            if rpt.contadorColor==0:
                               ec=0
                            else:                
                               ec=rpt.contadorColor-rpt.x_studio_lectura_anterior_color                                        
                            if rd.nombreAnte=='Renta base con ML incluidas BN o color + ML. excedentes' or rd.nombreAnte=='Renta base con páginas incluidas BN o color + pag. excedentes':
                                worksheet.write(i, 0, rpt.x_studio_indice,neg)
                                worksheet.write(i, 1, rpt.x_studio_locacin,neg)
                                worksheet.write(i, 2, rpt.x_studio_modelo,neg)
                                worksheet.write(i, 3, rpt.serie.name,neg)            
                                worksheet.write(i, 4, rpt.x_studio_lectura_anterior_bn,neg)
                                worksheet.write(i, 5, rpt.x_studio_lectura_anterior_color,neg)                        
                                worksheet.write(i, 6, rpt.contadorMono,neg)
                                worksheet.write(i, 7, rpt.contadorColor,neg)

                                worksheet.write(i, 15, rpt.x_studio_ubicacin,neg)
                                worksheet.write(i, 16, rpt.comentarioLecturas,neg)                                                            
                                worksheet.write(i, 8, ebn,neg)
                                worksheet.write(i, 9, ec,neg)
                                #worksheet.write(i, 10, ebn,neg)
                                #worksheet.write(i, 11, ec,neg)
                                eebn=ebn+eebn
                                eec=ec+eec
                                if str(rpt.serie.x_studio_estado)!='Back-up':
                                    if rpt.x_studio_color_o_bn=='B/N':                            
                                       if rd.bolsaBN<ebn:
                                          ebn=ebn-rd.bolsaBN
                                          #eebn=ebn+eebn  
                                          cal=float(rd.rentaMensual)+(ebn*rd.clickExcedenteBN)  
                                          worksheet.write(i, 12, cal,neg)
                                          worksheet.write(i, 10, ebn,neg)
                                          iva=round(cal*.16,2)
                                          worksheet.write(i, 13,'$ '+str(iva) ,neg)
                                          _logger.info('iva: ' + str(iva))
                                          _logger.info('cal: ' + str(cal))
                                          worksheet.write(i, 14,'$ '+str(iva +cal) ,neg)  
                                          ivatt=iva+ivatt  
                                          totalsr=(float(rd.rentaMensual)+(ebn*rd.clickExcedenteBN))+totalsr
                                          ttotal=(iva +cal)+ttotal
                                          _logger.info("totals si: " + str(totalsr))  
                                          _logger.info("tota si: " + str(ttotal))  
                                       else:                                                                                                         
                                          cal=float(rd.rentaMensual)
                                          worksheet.write(i, 12, cal,neg)
                                          iva=round(cal*.16,2)
                                          worksheet.write(i, 13,'$ '+str(iva) ,neg)
                                          worksheet.write(i, 14,'$ '+str(iva +cal) ,neg)  
                                          ivatt=iva+ivatt  
                                          totalsr=float(rd.rentaMensual)+totalsr
                                          ttotal=(iva +cal)+ttotal 
                                          _logger.info("totals elsebn: " + str(totalsr))  
                                          _logger.info("tota elsebn: " + str(ttotal))
                                    ebnx=0    
                                    if rpt.x_studio_color_o_bn=='Color':
                                       if rd.bolsaBN<ebn:
                                          ebn=ebn-rd.bolsaBN
                                          #eebn=ebn+eebn  
                                          ebnx=(ebn*rd.clickExcedenteBN)
                                          worksheet.write(i, 10, ebn,neg)  
                                          _logger.info("totals cnsi: " + str(totalsr))  
                                          _logger.info("tota cnsi: " + str(ttotal))     
                                       if rd.bolsaColor<ec:
                                          ec=ec-rd.bolsaColor
                                          #eec=ec+eec  
                                          call=float(rd.rentaMensual)+(ec*rd.clickExcedenteColor)+ebnx                                
                                          worksheet.write(i, 12, call,neg)
                                          worksheet.write(i, 11, ec,neg)
                                          iva=round(call*.16,2)
                                          ivatt=iva+ivatt
                                          worksheet.write(i, 13,'$ '+str(iva) ,neg)     
                                          worksheet.write(i, 14,'$ '+str(iva +call) ,neg)
                                          totalsr=call+totalsr
                                          ttotal=(iva +call)+ttotal
                                          _logger.info("totals csi: " + str(totalsr))  
                                          _logger.info("tota csi: " + str(ttotal))  
                                       else:
                                          _logger.info("totals celse: " + str(totalsr))  
                                          _logger.info("tota celse: " + str(ttotal))   
                                          call=float(rd.rentaMensual)+ebnx                                
                                          worksheet.write(i, 12, call,neg)
                                          iva=round(call*.16,2)
                                          ivatt=iva+ivatt
                                          worksheet.write(i, 13,'$ '+str(iva) ,neg)     
                                          worksheet.write(i, 14,'$ '+str(iva +call) ,neg)
                                          totalsr=call+totalsr
                                          ttotal=(iva +call)+ttotal
                                          _logger.info("totals celse: " + str(totalsr))  
                                          _logger.info("tota celse: " + str(ttotal))  

                                    _logger.info("totals f: " + str(totalsr))  
                                    _logger.info("tota fl: " + str(ttotal))  

                                i=i+1   
                            if rd.nombreAnte=='Costo por página procesada BN o color':
                                worksheet.write(i, 0, rpt.x_studio_indice,neg)
                                worksheet.write(i, 1, rpt.x_studio_locacin,neg)
                                worksheet.write(i, 2, rpt.x_studio_modelo,neg)
                                worksheet.write(i, 3, rpt.serie.name,neg)            
                                worksheet.write(i, 4, rpt.x_studio_lectura_anterior_bn,neg)
                                worksheet.write(i, 5, rpt.x_studio_lectura_anterior_color,neg)                        
                                worksheet.write(i, 6, rpt.contadorMono,neg)
                                worksheet.write(i, 7, rpt.contadorColor,neg)
                                worksheet.write(i, 8, ebn,neg)
                                worksheet.write(i, 9, ec,neg)
                                worksheet.write(i, 10, ebn,neg)
                                worksheet.write(i, 11, ec,neg)
                                worksheet.write(i, 15, rpt.x_studio_ubicacin,neg)
                                worksheet.write(i, 16, rpt.comentarioLecturas,neg)                                                            
                                if rpt.x_studio_color_o_bn=='B/N':                                    
                                   bs= (ebn*rd.clickExcedenteBN)
                                   eebn=ebn+eebn
                                   worksheet.write(i, 12, bs)
                                   iva=round(bs*.16,2)
                                   ivatt=iva+ivatt
                                   worksheet.write(i, 13,'$ '+str(iva) ,neg)
                                   worksheet.write(i, 14,'$ '+str(iva +bs) ,neg)
                                   totalsr=bs+totalsr
                                   ttotal=(iva +bs)+ttotal                        
                                if rpt.x_studio_color_o_bn=='Color':
                                   bsc=(ec*rd.clickExcedenteColor)+(ebn*rd.clickExcedenteBN)
                                   eec=ec+eec
                                   eebn=ebn+eebn 
                                   worksheet.write(i, 12, bsc,neg) 
                                   iva=round(bsc*.16,2)
                                   ivatt=iva+ivatt
                                   worksheet.write(i, 13,'$ '+str(iva) ,neg) 
                                   worksheet.write(i, 14,'$ '+str(iva +bsc) ,neg)
                                   totalsr=bsc+totalsr
                                   ttotal=(iva +bsc)+ttotal                                                                                                                  
                                i=i+1            
                            if rd.nombreAnte=='Renta base + costo de página procesada BN o color':
                                worksheet.write(i, 0, rpt.x_studio_indice,neg)
                                worksheet.write(i, 1, rpt.x_studio_locacin,neg)
                                worksheet.write(i, 2, rpt.x_studio_modelo,neg)
                                worksheet.write(i, 3, rpt.serie.name,neg)            
                                worksheet.write(i, 4, rpt.x_studio_lectura_anterior_bn,neg)
                                worksheet.write(i, 5, rpt.x_studio_lectura_anterior_color,neg)                        
                                worksheet.write(i, 6, rpt.contadorMono,neg)
                                worksheet.write(i, 7, rpt.contadorColor,neg)
                                worksheet.write(i, 8, ebn,neg)
                                worksheet.write(i, 9, ec,neg)
                                worksheet.write(i, 10, ebn,neg)
                                worksheet.write(i, 11, ec,neg)
                                worksheet.write(i, 15, rpt.x_studio_ubicacin,neg)
                                worksheet.write(i, 16, rpt.comentarioLecturas,neg)                                                            

                                if rpt.x_studio_color_o_bn=='B/N':              
                                   if str(rpt.serie.x_studio_estado)!='Back-up':
                                       bs= float(rd.rentaMensual)+(ebn*rd.clickExcedenteBN)
                                       eebn=ebn+eebn
                                       worksheet.write(i, 12, bs,neg)
                                       iva=round(bs*.16,2)
                                       ivatt=iva+ivatt
                                       worksheet.write(i, 13,'$ '+str(iva),neg )
                                       worksheet.write(i, 14,'$ '+str(iva +bs) ,neg)
                                       totalsr=bs+totalsr
                                       ttotal=(iva +bs)+ttotal
                                if rpt.x_studio_color_o_bn=='Color':
                                   if str(rpt.serie.x_studio_estado)!='Back-up': 
                                       bsc=float(rd.rentaMensual)+(ec*rd.clickExcedenteColor)+(ebn*rd.clickExcedenteBN)
                                       eec=ec+eec
                                       worksheet.write(i, 12, bsc,neg) 
                                       iva=round(bsc*.16,2)
                                       ivatt=iva+ivatt
                                       worksheet.write(i, 13,'$ '+str(iva) ,neg) 
                                       worksheet.write(i, 14,'$ '+str(iva +bsc) ,neg)
                                       totalsr=bsc+totalsr
                                       ttotal=(iva +bsc)+ttotal                                                                               
                                i=i+1

                for rd in re:            
                    if rd.nombreAnte=='SERVICIO DE PCOUNTER' or rd.nombreAnte=='SERVICIO DE PCOUNTER1' or rd.nombreAnte=='ADMINISTRACION DE DOCUMENTOS CON PCOUNTER' or rd.nombreAnte=='SERVICIO DE MANTENIMIENTO DE PCOUNTER' or rd.nombreAnte=='SERVICIO DE MANTENIMIENTO PCOUNTER' or rd.nombreAnte=='RENTA DE LICENCIAMIENTO PCOUNTER':
                       worksheet.write(i, 0, rd.nombreAnte,neg)
                       worksheet.write(i, 12, '$'+rd.rentaMensual,neg)
                       worksheet.write(i, 13, '$'+str(round(float(rd.rentaMensual)*.16,2)),neg)       
                       worksheet.write(i, 14, '$'+str(round(float(rd.rentaMensual)*.16,2)+float(rd.rentaMensual)),neg)
                       totalsr=float(rd.rentaMensual)+totalsr 
                       ivatt=round(float(rd.rentaMensual)*.16,2)+ivatt 
                       ttotal=(round(float(rd.rentaMensual)*.16,2)+float(rd.rentaMensual))+ttotal                                                
                    if rd.nombreAnte=='SERVICIO DE TFS' or rd.nombreAnte=='OPERADOR TFS' or rd.nombreAnte=='TFS' or rd.nombreAnte=='SERVICIO DE TFS ' :               
                       worksheet.write(i, 0, rd.nombreAnte,neg)
                       tfs=float(rd.rentaMensual)*int(rd.cantidad)               
                       retnecion=rd.retencion
                       rht=0
                       #raise exceptions.ValidationError("Nada que generar "+retnecion+" "+str(retnecion)!='N/A' )
                       if str(retnecion)!='N/A':
                          rht=float(rd.retencion)  
                       worksheet.write(i, 12, '$'+str(tfs),neg)
                       worksheet.write(i, 13, '$'+str(round(tfs*.16,2)),neg)                     
                       if rht>0:
                          worksheet.write(i, 15, 'Retencion $'+str(round(rht,2)),neg)
                          worksheet.write(i, 14, '$'+str(round(tfs*.16,2)+tfs),neg)
                          totalsr = tfs + totalsr
                          ttotal=round(tfs*.16,2)+tfs+ttotal-rht     
                       else:
                          worksheet.write(i, 14, '$'+str(round(tfs*.16,2)+tfs),neg)
                          totalsr = tfs + totalsr
                          ttotal=round(tfs*.16,2)+tfs+ttotal   

                       ivatt=round(float(tfs)*.16,2)+ivatt 



                    if rd.nombreAnte=='SERVICIO DE MANTENIMIENTO':                        
                       worksheet.write(i, 0, rd.nombreAnte,neg)
                       worksheet.write(i, 12, '$'+rd.rentaMensual,neg)
                       worksheet.write(i, 13, '$'+str(round(float(rd.rentaMensual)*.16,2)),neg)       
                       worksheet.write(i, 14, '$'+str(round(float(rd.rentaMensual)*.16,2)+float(rd.rentaMensual)),neg)
                       totalsr=float(rd.rentaMensual)+totalsr                 
                       ivatt=round(float(rd.rentaMensual)*.16,2)+ivatt 
                       ttotal=(round(float(rd.rentaMensual)*.16,2)+float(rd.rentaMensual))+ttotal
                    if rd.nombreAnte=='LECTORES DE PROXIMIDAD':                        
                       worksheet.write(i, 0, rd.nombreAnte,neg)
                       worksheet.write(i, 12, '$'+rd.rentaMensual,neg)
                       worksheet.write(i, 13, '$'+str(round(float(rd.rentaMensual)*.16,2)),neg)       
                       worksheet.write(i, 14, '$'+str(round(float(rd.rentaMensual)*.16,2)+float(rd.rentaMensual)),neg)
                       totalsr=float(rd.rentaMensual)+totalsr                 
                       ivatt=round(float(rd.rentaMensual)*.16,2)+ivatt 
                       ttotal=(round(float(rd.rentaMensual)*.16,2)+float(rd.rentaMensual))+ttotal            
                    if rd.nombreAnte=='PAPEL 350,000 HOJAS':                        
                       worksheet.write(i, 0, rd.nombreAnte,neg)
                       worksheet.write(i, 12, '$'+rd.rentaMensual,neg)
                       worksheet.write(i, 13, '$'+str(round(float(rd.rentaMensual)*.16,2)),neg)       
                       worksheet.write(i, 14, '$'+str(round(float(rd.rentaMensual)*.16,2)+float(rd.rentaMensual)),neg)
                       totalsr=float(rd.rentaMensual)+totalsr                 
                       ivatt=round(float(rd.rentaMensual)*.16,2)+ivatt 
                       ttotal=(round(float(rd.rentaMensual)*.16,2)+float(rd.rentaMensual))+ttotal
                    if rd.nombreAnte=='SOPORTE Y MANTENIMIENTO DE EQUIPOS':
                       importe=float(rd.rentaMensual)
                       worksheet.write(i, 0, rd.nombreAnte,neg)
                       worksheet.write(i, 12, '$'+str(importe),neg)
                       worksheet.write(i, 13, '$'+str(round(float(importe)*.16,2)),neg)       
                       worksheet.write(i, 14, '$'+str(round(float(importe)*.16,2)+float(importe)),neg)
                       totalsr=importe+totalsr                 
                       ivatt=round(float(importe)*.16,2)+ivatt                                
                       ttotal=(round(float(importe)*.16,2)+float(importe))+ttotal
                    if rd.nombreAnte=='SERVICIO DE ADMINISTRADOR KM NET MANAGER':
                       worksheet.write(i, 0, rd.nombreAnte,neg)
                       worksheet.write(i, 12, '$'+rd.rentaMensual,neg)
                       worksheet.write(i, 13, '$'+str(round(float(rd.rentaMensual)*.16,2)),neg)       
                       worksheet.write(i, 14, '$'+str(round(float(rd.rentaMensual)*.16,2)+float(rd.rentaMensual)),neg)
                       totalsr=float(rd.rentaMensual)+totalsr                                
                       ivatt=round(float(rd.rentaMensual)*.16,2)+ivatt 
                       ttotal=(round(float(rd.rentaMensual)*.16,2)+float(rd.rentaMensual))+ttotal
                    if rd.nombreAnte=='PAGINAS IMPRESAS EN BN ':
                       importe=float(rd.rentaMensual)*int(rd.cantidad)
                       worksheet.write(i, 0, rd.nombreAnte,neg)
                       worksheet.write(i, 12, '$'+str(importe),neg)
                       worksheet.write(i, 13, '$'+str(round(float(importe)*.16,2)),neg)       
                       worksheet.write(i, 14, '$'+str(round(float(importe)*.16,2)+float(importe)),neg)
                       totalsr=importe+totalsr                 
                       ivatt=round(float(importe)*.16,2)+ivatt                                
                       ttotal=(round(float(importe)*.16,2)+float(importe))+ttotal
                    if rd.nombreAnte=='RENTA MENSUAL DE LICENCIA  7 EMBEDED' or rd.nombreAnte=='RENTA MENSUAL DE LICENCIA  14 EMBEDED' or  rd.nombreAnte=='RENTA MENSUAL DE LICENCIA  2 EMBEDED':                        
                       worksheet.write(i, 0, rd.nombreAnte)
                       tfs=float(rd.rentaMensual)*int(rd.cantidad)
                       worksheet.write(i, 12, '$'+str(tfs),neg)
                       worksheet.write(i, 13, '$'+str(round(tfs*.16,2)),neg)       
                       worksheet.write(i, 14, '$'+str(round(tfs*.16,2)+tfs),neg)
                       totalsr = tfs + totalsr                                
                       ivatt=round(float(tfs)*.16,2)+ivatt 
                       ttotal=round(tfs*.16,2)+tfs+ttotal 

                    i=i+1    
                """
                    if rd.nombreAnte=='SERVICIO DE TFS' or rd.nombreAnte=='OPERADOR TFS' or rd.nombreAnte=='TFS' or rd.nombreAnte=='SERVICIO DE TFS ' :                        

                    if rd.nombreAnte=='SERVICIO DE MANTENIMIENTO':                        

                    if rd.nombreAnte=='SERVICIO DE ADMINISTRADOR KM NET MANAGER':                        

                    if rd.nombreAnte=='PAGINAS IMPRESAS EN BN':                        

                    if rd.nombreAnte=='RENTA MENSUAL DE LICENCIA  7 EMBEDED' or rd.nombreAnte=='RENTA MENSUAL DE LICENCIA  14 EMBEDED' or  rd.nombreAnte=='RENTA MENSUAL DE LICENCIA  2 EMBEDED':                        

                       for rpt in self.detalle :
                           if rpt.servicio==rd.id :
                                worksheet.write(i, 0, rpt.indice)
                                worksheet.write(i, 1, rpt.locacion)
                                worksheet.write(i, 2, rpt.modelo)
                                worksheet.write(i, 3, rpt.serieEquipo)            
                                worksheet.write(i, 4, rpt.lecturaAnteriorBN)
                                worksheet.write(i, 5, rpt.lecturaAnteriorColor)                        
                                worksheet.write(i, 6, rpt.ultimaLecturaBN)
                                worksheet.write(i, 7, rpt.ultimaLecturaColor)                                        
                                if rpt.ultimaLecturaBN==0:
                                   ebn=0
                                else:
                                   ebn=rpt.ultimaLecturaBN-rpt.lecturaAnteriorBN
                                if rpt.ultimaLecturaColor==0:
                                   ec=0
                                else:                
                                   ec=rpt.ultimaLecturaColor-rpt.lecturaAnteriorColor                    
                                worksheet.write(i, 15, rpt.ubi)                                                            
                                worksheet.write(i, 8, ebn)
                                worksheet.write(i, 9, ec)                                            
                                if rpt.bnColor=='B/N':                                                         
                                   eebn=ebn+eebn
                                if rpt.bnColor=='Color':                                                         
                                   eebn=ebn+eebn                                                                                   
                                   eec=ec+eec
                                i=i+1    
                       totalsr=float(rd.rentaMensual)+totalsr
                       ivatt=round(float(rd.rentaMensual)*.16,2)+ivatt
                       ttotal=round(float(rd.rentaMensual)*.16,2) +float(rd.rentaMensual)+ttotal
                """            
                worksheet.write(i, 10, eebn,neg)
                worksheet.write(i, 11, eec,neg)                
                worksheet.write(i, 12, '$'+str(round(totalsr,2)),neg)        
                worksheet.write(i, 13, '$'+str(round(ivatt,2)),neg)        
                worksheet.write(i, 14, '$'+str(round(ttotal,2)),neg)                
        workbook.close()
        data = open('Example2.xlsx', 'rb').read()
        base64_encoded = base64.b64encode(data).decode('UTF-8')

        self.excelD=base64_encoded


        
    

    """
    
    def carga_contadores(self):
        #ssc=self.env['contadores.contadores'].search([('cliente', '=', self.cliente.id),('mes', '=', self.mes),('anio', '=', self.anio),('id', '!=', self.id)],limit=1)        
       
        
        if self.anio and not self.csvD:
            perido=str(self.anio)+'-'+str(self.mes)
            periodoAnterior=''
            mesA=''
            anioA=''
            i=0
            for f in valores:                
                if f[0]==str(self.mes):                
                   mesaA=str(valores[i-1][0])
                i=i+1
            anios=get_years()
            i=0
            if str(self.mes)=='01':
               anioA=str(int(self.anio)-1)
            else:    
               anioA=str(self.anio)              
            periodoAnterior= anioA+'-'+mesaA   
            
            
            asdc=self.env['contrato'].search([('cliente','=',self.cliente.id)]).ids
            asds=self.env['servicios'].search([('contrato','in',asdc)]).ids
            asd=self.env['stock.production.lot'].search([('servicio','in',asds)])
            
            #raise exceptions.ValidationError("Nada que generar "+str(asd))                                     
            
            #raise Warning('notihng to show xD '+str(self.cliente.name))
            #id=int(self.id)            
            sc=self.env['contadores.contadores'].search([('id', '=', self.id)])
            sc.write({'name' : str(self.cliente.name)+' '+str(periodoAnterior)+' a '+str(perido)})
            i=1
            for a in asd:
                currentP=self.env['dcas.dcas'].search([('serie','=',a.id),('x_studio_field_no6Rb', '=', perido)],order='x_studio_fecha desc',limit=1)
                currentPA=self.env['dcas.dcas'].search([('serie','=',a.id),('x_studio_field_no6Rb', '=', periodoAnterior)],order='x_studio_fecha desc',limit=1)
                #raise exceptions.ValidationError("q onda xd"+str(self.id)+' id  '+str(id))                     
                if not currentP:
                   if a.servicio.id:
                      rrs=self.env['dcas.dcas'].create({'contador_id': self.id
                                                       , 'x_studio_producto': a.id
                                                       , 'serie': a.id
                                                       , 'x_studio_locacin':a.x_studio_locacion_recortada
                                                       , 'x_studio_ubicacin':a.x_studio_centro_de_costos
                                                       #, 'x_studio_periodo':str(self.anio)+ '-'+str(valores[int(self.mes)-1][1])                                                              
                                                       , 'x_studio_fecha_texto_anio':str(valores[int(self.mes)-1][1])+' de '+ str(self.anio)
                                                       ,'x_studio_field_no6Rb':str(self.anio)+'-'+str(self.mes)
                                                       , 'contadorMono': currentP.contadorMono
                                                       , 'x_studio_lectura_anterior_bn': currentPA.contadorMono
                                                       #, 'paginasProcesadasBN': bnp                                                   
                                                       , 'x_studio_periodo_anterior':str(valores[int(mesaA)-1][1])            + ' de '+ str(anioA)
                                                       , 'contadorColor': currentP.contadorColor
                                                       , 'x_studio_lectura_anterior_color': currentPA.contadorColor                                                             
                                                       #, 'paginasProcesadasColor': colorp
                                                       , 'x_studio_color_o_bn':a.x_studio_color_bn
                                                       , 'x_studio_indice': i
                                                       , 'x_studio_modelo':a.product_id.name
                                                       , 'x_studio_servicio':a.servicio.id
                                                       })
                
                else:
                   if a.servicio.id :
                      currentP.write({'contador_id': self.id
                                                       , 'x_studio_producto': a.id
                                                       , 'serie': a.id
                                                       , 'x_studio_locacin':a.x_studio_locacion_recortada
                                                       , 'x_studio_ubicacin':a.x_studio_centro_de_costos
                                                       , 'x_studio_fecha_texto_anio':str(valores[int(self.mes)-1][1])+' de '+ str(self.anio)
                                                       , 'x_studio_field_no6Rb':str(self.anio)+'-'+str(self.mes)
                                                       #, 'x_studio_periodo':str(self.anio)+ '-'+str(valores[int(self.mes)-1][1])                                                              
                                                       , 'contadorMono': currentP.contadorMono
                                                       , 'x_studio_lectura_anterior_bn': currentPA.contadorMono
                                                       #, 'paginasProcesadasBN': bnp                                                   
                                                       , 'x_studio_periodo_anterior':str(valores[int(mesaA)-1][1])+ ' de '+   str(anioA)          
                                                       , 'contadorColor': currentP.contadorColor
                                                       , 'x_studio_lectura_anterior_color': currentPA.contadorColor                                                             
                                                       #, 'paginasProcesadasColor': colorp
                                                       , 'x_studio_color_o_bn':a.x_studio_color_bn
                                                       , 'x_studio_indice': i
                                                       , 'x_studio_modelo':a.product_id.name
                                                       , 'x_studio_servicio':a.servicio.id
                                                        , 'x_studio_descripcin': 'capturado'
                                                       , 'x_studio_capturar':True
                                                       #,'id' : currentP.id
                                                       })
                
                i=1+i                
        if self.csvD:           
           with open("a1.csv","w") as f:
                f.write(base64.b64decode(self.csvD).decode("utf-8"))
           f.close()    
           file = open("a1.csv", "r")
           re = csv.reader(file)
           lista=list(re)
           j=0
           abuscar=[]
           sc=self.env['contadores.contadores'].search([('id', '=', self.id)])
           sc.write({'name' : "Carga por dca "})  
           for row in lista:                                            
               if j>0 :                                      
                   abuscar.append(row[3])
               j=j+1
           a=self.env['stock.production.lot'].search([('name','in',abuscar)])
           series=[]
           for t in a:                              
                for row in lista:
                    if t.name==row[3]:
                        #date = row[1]
                        #fecha = date.split('-')[0].split('/')
                        mes=(self.mes)
                        anio=str(self.anio)
                        i=0
                        for f in valores:                
                            if f[0]==str(mes):                
                               mesaA=str(valores[i-1][0])
                            i=i+1
                        anios=get_years()
                        i=0                  
                        if str(mes)=='01':
                           anioA=str(int(anio)-1)
                        else:    
                           anioA=str(anio)                    
                        periodoAnterior= anioA+'-'+mesaA
                        i=0
                        for f in valores:                
                            if f[0]==str(mes):                
                               mesaC=str(valores[i][0])
                            i=i+1                  
                        periodo= anio+'-'+mesaC                        
                        if row[7]=='':
                          bn=0
                        else:
                          bn=int(row[7])
                        if row[8]=='':
                          cc=0                    
                        else:
                          cc=int(row[8])                        
                        series.append({'serie': t.id
                                                 ,'contadorColor':cc
                                                 ,'contadorMono':bn
                                                 ,'fuente':'dcas.dcas'
                                                 ,'x_studio_field_no6Rb':periodo
                                                 ,'x_studio_fecha_texto_anio':str(valores[int(self.mes[1])-1][1])+' de '+str(self.anio)
                                                 ,'x_studio_descripcion':'cvs'
                                                 ,'x_studio_cliente':str(row[0])
                                                })                            
           self.env['dcas.dcas'].create(series)      
                        
            
        
            
            

    """
    
    def carga_contadores(self):
        #ssc=self.env['contadores.contadores'].search([('cliente', '=', self.cliente.id),('mes', '=', self.mes),('anio', '=', self.anio),('id', '!=', self.id)],limit=1)        
        """
        if ssc:
           self.sudo().unlink()                   
           url="https://gnsys-corp.odoo.com/web?#id="+str(ssc.id)+"&action=1129&model=contadores.contadores&view_type=form&menu_id=406"
           
           return {'name'     : 'Go to website',
                  'res_model': 'ir.actions.act_url',
                  'type'     : 'ir.actions.act_url',
                  'target'   : 'new',
                  'url'      : url
               } s     
        """
        
        if self.anio and not self.csvD:
            perido=str(self.anio)+'-'+str(self.mes)
            periodoAnterior=''
            mesA=''
            anioA=''
            i=0
            for f in valores:                
                if f[0]==str(self.mes):                
                   mesaA=str(valores[i-1][0])
                i=i+1
            anios=get_years()
            i=0
            if str(self.mes)=='01':
               anioA=str(int(self.anio)-1)
            else:    
               anioA=str(self.anio)              
            periodoAnterior= anioA+'-'+mesaA   
            
            
            asdc=self.env['contrato'].search([('cliente','=',self.cliente.id)]).ids
            asds=self.env['servicios'].search([('contrato','in',asdc)]).ids
            asd=self.env['stock.production.lot'].search([('servicio','in',asds)])
            
            #raise exceptions.ValidationError("Nada que generar "+str(asd))                                     
            
            #raise Warning('notihng to show xD '+str(self.cliente.name))
            #id=int(self.id)            
            sc=self.env['contadores.contadores'].search([('id', '=', self.id)])
            sc.write({'name' : str(self.cliente.name)+' '+str(periodoAnterior)+' a '+str(perido)})
            i=1
            for a in asd:
                currentP=self.env['dcas.dcas'].search([('serie','=',a.id),('x_studio_field_no6Rb', '=', perido)],order='x_studio_fecha desc',limit=1)
                currentPA=self.env['dcas.dcas'].search([('serie','=',a.id),('x_studio_field_no6Rb', '=', periodoAnterior)],order='x_studio_fecha desc',limit=1)
                #raise exceptions.ValidationError("q onda xd"+str(self.id)+' id  '+str(id))                     
                if not currentP:
                   if a.servicio.id:
                      rrs=self.env['dcas.dcas'].create({'contador_id': self.id
                                                       , 'x_studio_producto': a.id
                                                       , 'serie': a.id
                                                       #, 'x_studio_locacin':a.x_studio_locacion_recortada
                                                      #, 'x_studio_ubicacin':a.x_studio_centro_de_costos
                                                       #, 'x_studio_periodo':str(self.anio)+ '-'+str(valores[int(self.mes)-1][1])                                                              
                                                       , 'x_studio_fecha_texto_anio':str(valores[int(self.mes)-1][1])+' de '+ str(self.anio)
                                                       ,'x_studio_field_no6Rb':str(self.anio)+'-'+str(self.mes)
                                                       , 'contadorMono': currentP.contadorMono
                                                       , 'x_studio_lectura_anterior_bn': currentPA.contadorMono
                                                       #, 'paginasProcesadasBN': bnp                                                   
                                                       , 'x_studio_periodo_anterior':str(valores[int(mesaA)-1][1])            + ' de '+ str(anioA)
                                                       , 'contadorColor': currentP.contadorColor
                                                       , 'x_studio_lectura_anterior_color': currentPA.contadorColor                                                             
                                                       #, 'paginasProcesadasColor': colorp
                                                       #, 'x_studio_color_o_bn':a.x_studio_color_bn
                                                       , 'x_studio_indice': i
                                                       , 'x_studio_modelo':a.product_id.name
                                                       , 'x_studio_servicio':a.servicio.id
                                                       , 'x_studio_cliente':self.cliente.name 
                                                       })
                
                else:
                   if a.servicio.id :
                      currentP.write({'contador_id': self.id
                                                       , 'x_studio_producto': a.id
                                                       , 'serie': a.id
                                                       #, 'x_studio_locacin':a.x_studio_locacion_recortada
                                                       #, 'x_studio_ubicacin':a.x_studio_centro_de_costos
                                                       , 'x_studio_fecha_texto_anio':str(valores[int(self.mes)-1][1])+' de '+ str(self.anio)
                                                       , 'x_studio_field_no6Rb':str(self.anio)+'-'+str(self.mes)
                                                       #, 'x_studio_periodo':str(self.anio)+ '-'+str(valores[int(self.mes)-1][1])                                                              
                                                       , 'contadorMono': currentP.contadorMono
                                                       , 'x_studio_lectura_anterior_bn': currentPA.contadorMono
                                                       #, 'paginasProcesadasBN': bnp                                                   
                                                       , 'x_studio_periodo_anterior':str(valores[int(mesaA)-1][1])+ ' de '+   str(anioA)          
                                                       , 'contadorColor': currentP.contadorColor
                                                       , 'x_studio_lectura_anterior_color': currentPA.contadorColor                                                             
                                                       #, 'paginasProcesadasColor': colorp
                                                       #, 'x_studio_color_o_bn':a.x_studio_color_bn
                                                       , 'x_studio_indice': i
                                                       , 'x_studio_modelo':a.product_id.name
                                                       , 'x_studio_servicio':a.servicio.id
                                                        , 'x_studio_descripcion': 'capturado'
                                                       , 'x_studio_capturar':True
                                                       #,'id' : currentP.id
                                                       })
                
                i=1+i
            """retiros=self.env['sale.order'].search([('partner_id','=',self.cliente.id),('x_studio_tipo_de_solicitud', '=', 'Retiro'),('x_studio_cobrar_finiquito','=','True')])
            
            for re in retiros:
                #raise exceptions.ValidationError("faltan usocfdi para crear factura ")
                currentP=self.env['dcas.dcas'].search([('serie','=',re.serieRetiro2.id),('x_studio_field_no6Rb', '=', perido)],order='x_studio_fecha desc',limit=1)
                currentPA=self.env['dcas.dcas'].search([('serie','=',re.serieRetiro2.id),('x_studio_field_no6Rb', '=', periodoAnterior)],order='x_studio_fecha desc',limit=1)
                if not currentP:
                   #raise exceptions.ValidationError("faltan usocfdi para crear factura si")
                   if re.x_studio_field_69Boh.id:
                      rrs=self.env['dcas.dcas'].create({'contador_id': self.id
                                                       , 'x_studio_producto': re.serieRetiro2.id
                                                       , 'serie': re.serieRetiro2.id
                                                       , 'x_studio_locacin':re.partner_shipping_id.name
                                                       , 'x_studio_ubicacin':re.serieRetiro2.x_studio_centro_de_costos
                                                       #, 'x_studio_periodo':str(self.anio)+ '-'+str(valores[int(self.mes)-1][1])                                                              
                                                       , 'x_studio_fecha_texto_anio':str(valores[int(self.mes)-1][1])+' de '+ str(self.anio)
                                                       ,'x_studio_field_no6Rb':str(self.anio)+'-'+str(self.mes)
                                                       , 'contadorMono': currentP.contadorMono
                                                       , 'x_studio_lectura_anterior_bn': currentPA.contadorMono
                                                       #, 'paginasProcesadasBN': bnp                                                   
                                                       , 'x_studio_periodo_anterior':str(valores[int(mesaA)-1][1])            + ' de '+ str(anioA)
                                                       , 'contadorColor': currentP.contadorColor
                                                       , 'x_studio_lectura_anterior_color': currentPA.contadorColor                                                             
                                                       #, 'paginasProcesadasColor': colorp
                                                       , 'x_studio_color_o_bn':re.serieRetiro2.x_studio_color_bn
                                                       #, 'x_studio_indice': i
                                                       , 'x_studio_descripcion': 'Finiquito'
                                                       , 'x_studio_modelo':re.serieRetiro2.product_id.name
                                                       , 'x_studio_servicio':re.x_studio_field_69Boh.id
                                                       , 'x_studio_cliente':self.cliente.name  
                                                       })
               
                else:
                    if re.x_studio_field_69Boh.id :
                        #raise exceptions.ValidationError("faltan usocfdi para crear factura no")
                        currentP.write({'contador_id': self.id
                                                       , 'x_studio_producto': re.serieRetiro2.id
                                                       , 'serie': re.serieRetiro2.id
                                                       , 'x_studio_locacin':re.partner_shipping_id.name
                                                       , 'x_studio_ubicacin':re.serieRetiro2.x_studio_centro_de_costos
                                                       , 'x_studio_fecha_texto_anio':str(valores[int(self.mes)-1][1])+' de '+ str(self.anio)
                                                       , 'x_studio_field_no6Rb':str(self.anio)+'-'+str(self.mes)
                                                       #, 'x_studio_periodo':str(self.anio)+ '-'+str(valores[int(self.mes)-1][1])                                                              
                                                       , 'contadorMono': currentP.contadorMono
                                                       , 'x_studio_lectura_anterior_bn': currentPA.contadorMono
                                                       #, 'paginasProcesadasBN': bnp                                                   
                                                       , 'x_studio_periodo_anterior':str(valores[int(mesaA)-1][1])+ ' de '+   str(anioA)          
                                                       , 'contadorColor': currentP.contadorColor
                                                       , 'x_studio_lectura_anterior_color': currentPA.contadorColor                                                             
                                                       #, 'paginasProcesadasColor': colorp
                                                       , 'x_studio_color_o_bn':re.serieRetiro2.x_studio_color_bn
                                                       , 'x_studio_indice': i
                                                       , 'x_studio_modelo':re.serieRetiro2.product_id.name
                                                       , 'x_studio_servicio':re.x_studio_field_69Boh.id
                                                       , 'x_studio_descripcion': 'capturado Finiquito'
                                                       , 'x_studio_capturar':True                                                                                               
                                                       })
            """        
        if self.csvD:           
           with open("a1.csv","w") as f:
                f.write(base64.b64decode(self.csvD).decode("utf-8"))
           f.close()    
           file = open("a1.csv", "r")
           re = csv.reader(file)
           lista=list(re)
           j=0
           abuscar=[]
           sc=self.env['contadores.contadores'].search([('id', '=', self.id)])
           sc.write({'name' : "Carga por dca "})  
           for row in lista:                                            
               if j>0 :                                      
                   abuscar.append(row[3])
               j=j+1
           a=self.env['stock.production.lot'].search([('name','in',abuscar)])
           series=[]
           for t in a:                              
                for row in lista:
                    if t.name==row[3]:
                        #date = row[1]
                        #fecha = date.split('-')[0].split('/')
                        mes=(self.mes)
                        anio=str(self.anio)
                        i=0
                        for f in valores:                
                            if f[0]==str(mes):                
                               mesaA=str(valores[i-1][0])
                            i=i+1
                        anios=get_years()
                        i=0                  
                        if str(mes)=='01':
                           anioA=str(int(anio)-1)
                        else:    
                           anioA=str(anio)                    
                        periodoAnterior= anioA+'-'+mesaA
                        i=0
                        for f in valores:                
                            if f[0]==str(mes):                
                               mesaC=str(valores[i][0])
                            i=i+1                  
                        periodo= anio+'-'+mesaC                        
                        if row[7]=='':
                          bn=0
                        else:
                          bn=int(row[7])
                        if row[8]=='':
                          cc=0                    
                        else:
                          cc=int(row[8])                        
                        series.append({'serie': t.id
                                                 ,'contadorColor':cc
                                                 ,'contadorMono':bn
                                                 ,'fuente':'dcas.dcas'
                                                 ,'x_studio_field_no6Rb':periodo
                                                 ,'x_studio_fecha_texto_anio':str(valores[int(self.mes[1])-1][1])+' de '+str(self.anio)
                                                 ,'x_studio_descripcion':'cvs'
                                                 ,'x_studio_cliente':str(row[0])
                                                })                            
           self.env['dcas.dcas'].create(series)      
                            
        
        
        
    #@api.onchange('archivo')
    def onchange_archiv(self):
        f=open('1.txt','w')
        for record in self:
            if record.archivo:
                s=base64.b64decode(record.archivo)
                cv1=io.StringIO(str(s))
                #writer = csv.writer(cv1, dialect='excel', delimiter=',')
                split=str(s).split('\\n')
                #split=str(s).split('\n')
                i=0
                for sp in split:
                    if(i>0):
                        dat=sp.split(' - ',1)
                        campos=dat[1].split(',')
                        p=self.env['res.partner'].search([['name','=',dat[0]]])
                        h=self.env['res.partner'].search([['name','=',campos[0]],['parent_id','=',p.id]])
                        t=self.env['stock.production.lot'].search([['name','=',campos[3]]])
                        f.write(str(len(t))+'\n')
                    i=i+1
        f.close()
                        #record.dca.search([['serial.name','=',dat[3]]])

    detalle =  fields.One2many('contadores.contadores.detalle', 'contadores', string='Contadores')
   





class detalleContadores(models.Model):
      _name = 'contadores.contadores.detalle'
      _description = 'Detalle Contadores'
     
      contadores = fields.Many2one('contadores.contadores', string='Detalle de contadores')
      contadoresexcel = fields.Many2one('contadores.excel', string='Detalle de contadores csv')
     
      serieEquipo = fields.Text(string="Serie")
      producto = fields.Text(string="Producto")
      locacion = fields.Text(string="Locación")
      capturar = fields.Boolean()     
      bnColor = fields.Text(string='Equipo B/N o Color')  
      ultimaLecturaBN = fields.Integer(string='Última lectura monocromatico')
      lecturaAnteriorBN = fields.Integer(string='Lectura anterior monocromatico')
      paginasProcesadasBN = fields.Integer(string='Páginas procesadas monocromatico')
      indice = fields.Integer(string='índice')
     
      ultimaLecturaColor = fields.Integer(string='última lectura color')
      lecturaAnteriorColor = fields.Integer(string='Lectura anterior color')
      paginasProcesadasColor = fields.Integer(string='Páginas procesadas color')
     
      periodo = fields.Text(string="Periodo")
      periodoA = fields.Text(string="Periodo Anterior")
      comentario = fields.Text(string="Comentario")
      archivo=fields.Binary(store='True',string='Archivo')
      modelo=fields.Text(string="Modelo")
      ubi=fields.Text(string="Ubicacion")
      servicio=fields.Integer(string='Servicio')
      desc=fields.Text(string="Descripcion",readonly="1")  
        


        
        
   

    
    
    
class contadores_lines(models.Model):
    _name="contadores.lines"
    _description = "lineas contadores"
    serie=fields.Many2one('stock.production.lot')
    ticket=fields.Many2one('contadores.contadores',string='Order Reference')
    contadorAnterior=fields.Many2one('dcas.dcas',string='Anterior',compute='ultimoContador')
    contadorColor=fields.Integer(string='Contador Color')
    contadorNegro=fields.Integer(string='Contador Monocromatico')
    contadorAnteriorMono=fields.Integer(related='contadorAnterior.contadorMono',string='Anterior Monocromatico')
    contadorAnteriorColor=fields.Integer(related='contadorAnterior.contadorColor',string='Anterior Color')
    cliente=fields.Many2one('res.partner')
    nombre=fields.Char(related='cliente.name',string='Nombre Cliente')
    mes=fields.Integer()
    pagina=fields.Binary('Pagina de Estado')
    
    #@api.depends('serie')
    def ultimoContador(self):
        fecha=datetime.datetime.now()
        for record in self:
            if(record.serie):
                dc=self.env['dcas.dcas'].search([('fuente','=','dcas.dcas'),('x_studio_fecha_techra','!=',False),('serie','=',record.serie.id)]).sorted(key='x_studio_fecha_techra')
                if(len(dc)>1):
                    record['contadorAnterior']=dc[0].id
        
class lor(models.Model):
    _inherit = 'stock.production.lot'
    dca=fields.One2many('dcas.dcas',inverse_name='serie')

    instalado_el = fields.Datetime(string = 'Fecha de instalación', store=True)
    html = fields.Text(string = 'Tickets', compute = 'gener_tabla_tickets')

    

    x_studio_estado = fields.Selection([["Obsoleto","Obsoleto"],["Usado","Usado"],["Hueso","Hueso"],["Para reparación","Para reparación"],["Nuevo","Nuevo"],["Buenas condiciones","Buenas condiciones"],["Excelentes condiciones","Excelentes condiciones"],["Back-up","Back-up"],["Dañado","Dañado"]], store=True, track_visibility='onchange')
    x_studio__amarrillo = fields.Integer(store=True, string='% Amarrillo')
    x_studio__cian = fields.Integer(store=True, string='& cian')
    x_studio__magenta = fields.Integer(store=True, string='% Magenta')
    x_studio__negro = fields.Integer(store=True, string='% negro')
    x_studio_activo = fields.Boolean(store=True, string='Activo')
    x_studio_amarillo = fields.Char(store=True, readonly=True, string='Amarillo', compute = '_compute_x_studio_amarillo')

    @api.depends('dca')
    def _compute_x_studio_amarillo(self):
      for record in self:
        if len(record.dca) > 0:
          cont_color = str(record.dca[len(record.dca) - 1].porcentajeAmarillo)
          record['x_studio_amarillo'] = str(cont_color) 

    x_studio_amarillo_anterior = fields.Char(store=True, readonly=True, string='Amarillo Anterior', compute = '_compute_x_studio_amarillo_anterior')

    @api.depends('dca')
    def _compute_x_studio_amarillo_anterior(self):
      for record in self:
        if len(record.dca) > 0:
          cont_color = str(record.dca[len(record.dca) - 2].porcentajeAmarillo)
          record['x_studio_amarillo_anterior'] = str(cont_color) 

    x_studio_arreglo = fields.Char(store=True, string='arreglo')
    x_studio_calle = fields.Char(store=False, readonly=True, string='calle')
    x_studio_cambiar = fields.Boolean(store=True, string='Cambiar')
    x_studio_cambio = fields.Boolean(store=True, string='Cambiar', track_visibility = 'onchange')
    x_studio_categoria_de_producto = fields.Many2one('product.category',string='Categoría de producto',store=True)
    x_studio_categoria_de_producto_3 = fields.Many2one('product.category',string='Categoría de producto',store=True)
    x_studio_centro_de_costos = fields.Char(store=False, string='Ubicación')

    x_studio_cian_1 = fields.Char(store=True, readonly=True, string='Cian', compute = '_compute_x_studio_cian_1')

    @api.depends('dca')
    def _compute_x_studio_cian_1(self):
      for record in self:
        if len(record.dca) > 0:
          cont_color = str(record.dca[len(record.dca) - 1].porcentajeCian)
          record['x_studio_cian_1'] = str(cont_color) 

    x_studio_cian_anteior = fields.Char(store=True, readonly=True, string='Cian Anteior', compute = '_compute_x_studio_cian_anteior')

    @api.depends('dca')
    def _compute_x_studio_cian_anteior(self):
      for record in self:
        if len(record.dca) > 0:
          cont_color = str(record.dca[len(record.dca) - 2].porcentajeCian)
          record['x_studio_cian_anteior'] = str(cont_color) 

    x_studio_ciudad = fields.Char(readonly=False, string='Ciudad')
    x_studio_cliente = fields.Many2one('res.partner',string='Cliente',store=True, track_visibility = 'onchange')
    x_studio_colonia = fields.Char(readonly=True, string='Colonia')

    """
    x_studio_color_bn = fields.Selection([['B/N', 'B/N'], ['Color', 'Color']], readonly=True, store=True, string='Color B/N')
    
    Falta migrar a odoo 14
    """
    x_studio_color_bn = fields.Selection([['B/N', 'B/N'], ['Color', 'Color']], readonly=True, store=False, string='Color B/N', compute='_compute_x_studio_color_bn')
    @api.depends('product_id')
    def _compute_x_studio_color_bn(self):
        #self.x_studio_color_bn = None
        for record in self:
            if record.product_id.id:
                record['x_studio_color_bn'] = record.product_id.x_studio_color_bn
    


    x_studio_colorestoner = fields.Char(readonly=True, store=True, string='colorestoner', track_visibility = 'onchange')
    x_studio_comentario = fields.Text(string = 'Comentario', store = True)
    x_studio_contador_bn = fields.Char(readonly=True, string='Contador B/N', compute = '_compute_x_studio_contador_bn')

    @api.depends('dca')
    def _compute_x_studio_contador_bn(self):
      for record in self:
        t=len(record.dca)
        h=[]
        d=''
        f=0
        if t > 0:
          for a in record.dca :
            d=str(a.fuente)
            if d=='helpdesk.ticket': 
               h.append(a.contadorMono)
            if len(h)==0:
              f=0
            if len(h)>1:
              f=max(h)
            if len(h)==1:
              f=h[0]  
          record['x_studio_contador_bn'] = f
        else:
          record['x_studio_contador_bn'] = 0

    x_studio_contador_bn_a_capturar = fields.Integer(store=True, string='Contador B/N a capturar')
    x_studio_contador_bn_anterior = fields.Char(readonly=True, string='Contador B/N anterior', compute = '_compute_x_studio_contador_bn_anterior')

    @api.depends('dca')
    def _compute_x_studio_contador_bn_anterior(self):
      for record in self:
        record['x_studio_contador_bn_anterior'] = 0

    x_studio_contador_bn_mesa = fields.Integer(store=True, readonly=True, string='Contador BN Mesa', compute = '_compute_x_studio_contador_bn_mesa')

    @api.depends('dca')
    def _compute_x_studio_contador_bn_mesa(self):
      for record in self:
        t=len(record.dca)
        h=[]
        d=''
        f=0
        if t > 0:
          for a in record.dca :
            d=str(a.fuente)
            if d=='helpdesk.ticket': 
               h.append(a.contadorMono)
            if len(h)==0:
              f=0
            if len(h)>1:
              f=max(h)
            if len(h)==1:
              f=h[0]  
          record['x_studio_contador_bn_mesa'] = f
        else:
          record['x_studio_contador_bn_mesa'] = 0

    x_studio_contador_bn_mesa__1 = fields.Integer(store=True, string='Contador BN Mesa')
    x_studio_contador_color = fields.Char(default=0, readonly=True, string='Contador Color', compute = '_compute_x_studio_contador_color')

    @api.depends('dca')
    def _compute_x_studio_contador_color(self):
      self.x_studio_contador_color = 0
      for record in self:
        t=len(record.dca)
        h=[]
        
        if t > 0:
          for a in record.dca :
            d=str(a.fuente)
            if d=='helpdesk.ticket': 
              h.append(a.contadorColor)
          #m=max(h)
          if len(h)==0:
           record['x_studio_contador_color'] = 0
          else:
           record['x_studio_contador_color'] = max(h)

    x_studio_contador_color_a_capturar = fields.Integer(store=True, string='Contador color a capturar')
    x_studio_contador_color_anterior = fields.Char(readonly=True, string='Contador Color anterior', compute = '_compute_x_studio_contador_color_anterior')

    @api.depends('dca')
    def _compute_x_studio_contador_color_anterior(self):
      for record in self:
        record['x_studio_contador_color_anterior'] = 0

    x_studio_contador_color_mesa = fields.Integer(readonly=True, string='Contador Color Mesa', compute = '_compute_x_studio_contador_color_mesa')

    @api.depends('dca')
    def _compute_x_studio_contador_color_mesa(self):
      for record in self:
        t=len(record.dca)
        h=[]
        d=''
        f=0
        if t > 0:
          for a in record.dca :
            d=str(a.fuente)
            if d=='helpdesk.ticket': 
               h.append(a.contadorColor)
            if len(h)==0:
              f=0
            if len(h)>1:
              f=max(h)
            if len(h)==1:
              f=h[0]  
          record['x_studio_contador_color_mesa'] = f
        else:
          record['x_studio_contador_color_mesa'] = 0

    x_studio_contador_kit_mantenimiento = fields.Integer(store=True, string='Contador kit mantenimiento')
    x_studio_contador_mesa_bn = fields.Integer(readonly=True, string='Contador Mesa BN', compute = '_compute_x_studio_contador_mesa_bn')

    @api.depends('dca')
    def _compute_x_studio_contador_mesa_bn(self):
      for record in self:
        t=len(record.dca)
        h=[]
        d=''
        f=0
        if t > 0:
          for a in record.dca :
            d=str(a.fuente)
            if d=='helpdesk.ticket': 
               h.append(a.contadorMono)
            if len(h)==0:
              f=0
            if len(h)>1:
              f=max(h)
            if len(h)==1:
              f=h[0]  
          record['x_studio_contador_mesa_bn'] = f
        else:
          record['x_studio_contador_mesa_bn'] = 0

    x_studio_contador_mesa_color = fields.Integer(store=True, string='Contador mesa color')
    x_studio_contador_rodillo = fields.Integer(store=True, string='Contador rodillo')
    x_studio_contador_unidad_de_imagen = fields.Integer(store=True, string='Contador unidad de imagen')
    """
    x_studio_contrato = fields.Char(readonly=True, string='Contrato', compute = '_compute_x_studio_contrato')

    @api.depends('servicio')
    def _compute_x_studio_contrato(self):
      for r in self:
        if r.servicio:
          r['x_studio_contrato']=str(r.servicio.contrato.idTechraRef)
    """
    x_studio_cp = fields.Char(readonly=True, store=False, string='CP')
    x_studio_currentuser = fields.Char(readonly=True, string='currentUser', compute = '_compute_x_studio_currentuser')

    @api.depends('x_studio_currentuser')
    def _compute_x_studio_currentuser(self):
      for t in self:
        t['x_studio_currentuser'] = self.env.user.name


    x_studio_d_envio = fields.Char(readonly=True, store=False, string='d envio')
    x_studio_dcas_penultimo = fields.Char(readonly=True, store=True, string='DCAS penultimo', compute = '_compute_x_studio_dcas_penultimo')

    @api.depends('dca')
    def _compute_x_studio_dcas_penultimo(self):
      for record in self:
        if len(record.dca) > 0:
          cont_mono = str(record.dca[len(record.dca) - 2].contadorMono)
          cont_color = str(record.dca[len(record.dca) - 2].contadorColor)
          cont_color_negro = str(record.dca[len(record.dca) - 2].porcentajeNegro)
          cont_color_magenta = str(record.dca[len(record.dca) - 2].porcentajeMagenta)
          cont_color_amarillo = str(record.dca[len(record.dca) - 2].porcentajeAmarillo)
          cont_color_cyan = str(record.dca[len(record.dca) - 2].porcentajeCian)
          record['x_studio_dcas_penultimo'] = 'último Contador monocormatico '+cont_mono + ' último Contador color '+  cont_color + ' último procentaje negro '+  cont_color_negro +' último procentaje magenta ' + cont_color_magenta + ' último procentaje amarillo ' + cont_color_amarillo + ' último procentaje cyan ' + cont_color_cyan
    
    x_studio_dcas_ultimo = fields.Char(readonly=True, store=True, string='DCAS ultimo', compute = '_compute_x_studio_dcas_ultimo')

    @api.depends('dca')
    def _compute_x_studio_dcas_ultimo(self):
      for record in self:
        if len(record.dca) > 0:
          cont_mono = str(record.dca[len(record.dca) - 1].contadorMono)
          cont_color = str(record.dca[len(record.dca) - 1].contadorColor)
          cont_color_negro = str(record.dca[len(record.dca) - 1].porcentajeNegro)
          cont_color_magenta = str(record.dca[len(record.dca) - 1].porcentajeMagenta)
          cont_color_amarillo = str(record.dca[len(record.dca) - 1].porcentajeAmarillo)
          cont_color_cyan = str(record.dca[len(record.dca) - 1].porcentajeCian)
          record['x_studio_dcas_ultimo'] = 'último Contador monocormatico '+cont_mono + ' último Contador color '+  cont_color + ' último procentaje negro '+  cont_color_negro +' último procentaje magenta ' + cont_color_magenta +  ' último procentaje amarillo ' + cont_color_amarillo + ' último procentaje cyan ' + cont_color_cyan
    
    x_studio_delegacion = fields.Char(readonly=True, store=False, string='delegacion')
    x_studio_demo = fields.Boolean(store=True, string='Demo', track_visibility = 'onchange')
    x_studio_equipo = fields.Char(readonly=True, store=False, string='equipo')
    x_studio_esconde = fields.Char(store=False, copied = True, string='esconde')
    x_studio_estado = fields.Selection([["Obsoleto","Obsoleto"],["Usado","Usado"],["Hueso","Hueso"],["Para reparación","Para reparación"],["Nuevo","Nuevo"],["Buenas condiciones","Buenas condiciones"],["Excelentes condiciones","Excelentes condiciones"],["Back-up","Back-up"],["Dañado","Dañado"]], store=True, string = 'Estado', track_visibility = 'onchange')
    x_studio_estado_1 = fields.Char(readonly=True, store=False, string='Estado')
    x_studio_etapa = fields.Selection([["Almacen","Almacen"],["Distribución","Distribución"],["Ruta","Ruta"]], store=True, string = 'Etapa')
    x_studio_evidencias = fields.Binary(string='Evidencias', store=True)
    x_studio_evidencias_filename = fields.Char(store=True, string='Filename for x_studio_evidencias')
    x_studio_exterior = fields.Char(readonly=True, string='Exterior')
    x_studio_fecha_lectura_actual = fields.Char(readonly=True, store=True, string='Fecha lectura actual', compute = '_compute_x_studio_fecha_lectura_actual')

    @api.depends('dca')
    def _compute_x_studio_fecha_lectura_actual(self):
        self.x_studio_fecha_lectura_actual = ''
        for record in self:
            if len(record.dca) > 0:
                fecha = str(record.dca[len(record.dca) - 2].create_date)
                record['x_studio_fecha_lectura_actual'] = fecha

    x_studio_fecha_ultima_lectura = fields.Char(readonly=True, store=True, string='Fecha última lectura', compute = '_compute_x_studio_fecha_ultima_lectura')

    @api.depends('dca')
    def _compute_x_studio_fecha_ultima_lectura(self):
        self.x_studio_fecha_ultima_lectura = ''
        for record in self:
            if len(record.dca) > 0:
                fecha = str(record.dca[len(record.dca) - 1].create_date)
                record['x_studio_fecha_ultima_lectura'] = fecha

    x_studio_field_06Xvu = fields.Integer(store=True, string='New Número entero')
    #x_studio_field_17hqX = fields.Integer(store=True, readonly=True, related='x_studio_field_a9oR8.id', string='New Related Field')
    x_studio_field_2MXvT = fields.Many2one('helpdesk.ticket',string='Tiquete del Servicio de Asistencia',store=True)
    x_studio_field_3OnO2 = fields.Many2one('dcas.dcas',string='DCAS primero',store=True, copied=True, compute = '_compute_x_studio_field_3OnO2')

    @api.depends('dca')
    def _compute_x_studio_field_3OnO2(self):
      for record in self:
        if len(record.dca) > 0:
          record['x_studio_field_3OnO2'] = record.dca[len(record.dca) - 1].id

    x_studio_field_4TVx2 = fields.Integer(store=True, string='New Número entero')
    x_studio_field_6HFrO = fields.Many2one('product.category',string='New Campo relacionado',store=True)
    x_studio_field_8tSxH = fields.Selection([['SOPORTE Y MANTENIMIENTO DE EQUIPOS', 'SOPORTE Y MANTENIMIENTO DE EQUIPOS'], ['SERVICIO DE ADMINISTRADOR KM NET MANAGER', 'SERVICIO DE ADMINISTRADOR KM NET MANAGER'], ['Costo por página procesada BN o color', 'Costo por página procesada BN o color'], ['RENTA MENSUAL DE LICENCIA EMBEDED', 'RENTA MENSUAL DE LICENCIA EMBEDED'], ['Renta base con ML incluidas BN o color + ML. excedentes', 'Renta base con ML incluidas BN o color + ML. excedentes'], ['TFS', 'TFS'], ['SERVICIO DE PCOUNTER', 'SERVICIO DE PCOUNTER'], ['Renta global + costo de página procesada BN o color', 'Renta global + costo de página procesada BN o color'], ['Renta global con páginas incluidas BN o color + pag. Excedentes', 'Renta global con páginas incluidas BN o color + pag. Excedentes'], ['Renta base + costo de página procesada BN o color', 'Renta base + costo de página procesada BN o color'], ['PAGINAS IMPRESAS EN BN', 'PAGINAS IMPRESAS EN BN']], store=True, readonly=True, string = 'New Campo relacionado', track_visibility = 'always')
    
    

    x_studio_field_A6PR9 = fields.Char(readonly=True, store=False, string='Color Tóner', compute = '_compute_x_studio_field_A6PR9')

    @api.depends('x_studio_toner_compatible')
    def _compute_x_studio_field_A6PR9(self):
        self.x_studio_field_A6PR9 = ''
        for record in self:
            record['x_studio_field_A6PR9'] = record.x_studio_toner_compatible.x_studio_color

    x_studio_contrato = fields.Char(readonly=True, store=False, string='Contrato', compute = '_compute_x_studio_contrato')

    @api.depends('servicio')
    def _compute_x_studio_contrato(self):
        self.x_studio_contrato = ''
        for r in self:
            if r.servicio:
                r['x_studio_contrato']=str(r.servicio.contrato.idTechraRef)
    
    #x_studio_field_B7uLt = fields.One2many('x_dcas','x_studio_field_ue4Ea', string='DCAS')
    """
    x_studio_field_GCPuy = 
    x_studio_field_Hqyl6)
    x_studio_field_K5APD)
    x_studio_field_L0MFC)
    x_studio_field_LV0Ls)
    x_studio_field_OLXDH)
    x_studio_field_OnbMI)
    """
    x_studio_field_PYss4 = fields.One2many('dcas.dcas','serie', string='Lecturas', store=True, domain='[["fuente","=","dcas.dcas"]]')
    """
    x_studio_field_PwHLb)
    """
    x_studio_field_Q3Qpi = fields.Many2many('sale.order', relation ='x_sale_order_stock_production_lot_rel', column1='stock_production_lot_id', column2='sale_order_id', string='Pedido de venta', store=True)
    """
    x_studio_field_QwAZL)
    x_studio_field_RJsuy)
    x_studio_field_SOEw0)
    x_studio_field_T6sqp)
    x_studio_field_T7oRn)
    x_studio_field_T7oRn_filename)
    x_studio_field_U8OZg)
    x_studio_field_X8DSD)
    x_studio_field_XUPMG)
    x_studio_field_YleJ2)
    """
    x_studio_field_Yxv2m = fields.One2many('dcas.dcas','serie', string='New UnoAMuchos', store=True)
    
    x_studio_field_Zi7sY = fields.Many2one('product.product',string='Producto',store=True)

    """
    x_studio_field_ZwQ81)
    """
    #x_studio_field_a9oR8 = fields.Many2one('helpdesk.ticket',string='Tiquete del Servicio de Asistencia',store=True)
    """
    x_studio_field_alFCw_filename)
    x_studio_field_bh9t3)
    x_studio_field_dyZzv)
    x_studio_field_fBLGz)
    x_studio_field_jBvLz)
    x_studio_field_kgrzI)
    """
    x_studio_field_lMCjm = fields.Many2many(comodel_name='product.product', string='Producto', store=True)

    """
    x_studio_field_lVjdA)
    x_studio_field_nXQHF)
    x_studio_field_nbkyC)
    x_studio_field_nrBXH)
    x_studio_field_oRtcm)
    x_studio_field_pnM9a)
    x_studio_field_tLm45)
    x_studio_field_uNrUk)
    x_studio_field_vJQCQ)
    x_studio_field_x7TId)
    x_studio_field_xNRsI)
    x_studio_field_zAuUJ)
    x_studio_field_zQZRw)
    
    x_studio_helpdesk_team_id)
    """
    #x_studio_histrico_de_componentes = fields.One2many('x_studio_historico_de_componentes','x_studio_field_MH4DO', string='Histórico De Componentes ', store=True, domain='["|",("x_ultimaCargaRefacciones","=",True),("x_studio_modelo","like","Refacción y/o accesorio:")]')
    
    x_studio_idotrosistmp = fields.Char(string='idotrosistmp', store=True)
    servicio = fields.Many2one('servicios',string='Servicio serie',store=True, copied=True)
    x_studio_idreal = fields.Char(string='idreal', readonly=True, compute='_compute_x_studio_idreal')

    @api.depends('servicio')
    def _compute_x_studio_idreal(self):
        self.x_studio_idreal = ''
        for r in self:
            if r.servicio.id:
                r['x_studio_idreal']=str(r.servicio.idtec)

    
    x_studio_suscripcion = fields.Many2one('_unknown', string='Suscripción', store=True)
    
    x_studio_idservicio = fields.Char(string='idservicio', readonly=True, compute='_compute_x_studio_idservicio')

    @api.depends('x_studio_suscripcion')
    def _compute_x_studio_idservicio(self):
        self.x_studio_idservicio = ''
        for r in self:
            if r.x_studio_suscripcion.id:
                r['x_studio_idservicio']=str(r.x_studio_suscripcion.id)
    

    #x_studio_idticket = fields.Integer(string='idticket', readonly=True, store=True, related='x_studio_field_a9oR8.x_studio_id_ticket')
    x_studio_idtoner = fields.Char(string='idservicio', readonly=True, store=True, compute='_compute_x_studio_idtoner')

    @api.depends('x_studio_toner_compatible')
    def _compute_x_studio_idtoner(self):
        self.x_studio_idtoner = ''
        for record in self:
            if record.x_studio_toner_compatible.id:
                record['x_studio_idtoner'] = record.x_studio_toner_compatible.id

    x_studio_impresiones = fields.Integer(string='Impresiones Facturación', readonly=True, compute='_compute_x_studio_impresiones')

    @api.depends('dca')
    def _compute_x_studio_impresiones(self):
        for record in self:
            record['x_studio_impresiones'] = 0
    """
    x_studio_impresiones_color
    x_studio_impresiones_color_mesa)
    x_studio_impresiones_color_mesa_1)
    x_studio_impresiones_mesa)
    x_studio_impresiones_tner)
    """
    x_studio_instalado = fields.Boolean(string='Instalado', store=True)
    
    x_studio_interior = fields.Char(string='Interior', readonly=True)
    
    x_studio_lec_ant_bn = fields.Integer(string='Lec. Ant. BN', readonly=True)
    
    x_studio_lec_ant_color = fields.Integer(string='Lec. Ant. color', readonly=True)
    x_studio_ultima_ubicacin = fields.Char(readonly=True, store=False, string='Ultima Ubicación')
    
    """
    Falta migrar a odoo 14
    x_studio_ultima_ubicacin = fields.Char(readonly=True, store=False, string='Ultima Ubicación', compute = '_compute_x_studio_ultima_ubicacin')
    @api.depends('x_studio_cambio')
    def _compute_x_studio_ultima_ubicacin(self):
        self.x_studio_ultima_ubicacin = ''
        self.x_studio_delegacion = ''
        for r in self:
            tam = len(r.x_studio_move_line)
            pos = tam-1
            if r.x_studio_localidad_2.id:
                loca = r.x_studio_localidad_2
                r['x_studio_ultima_ubicacin'] = str(loca.display_name)
                r['x_studio_delegacion'] = str(loca.l10n_mx_edi_locality)
    """

    x_studio_locacion_recortada = fields.Char(readonly=True, store=False, string='Locación', compute = '_compute_x_studio_locacion_recortada')

    @api.depends('x_studio_localidad_2')
    def _compute_x_studio_locacion_recortada(self):
        self.x_studio_locacion_recortada = ''
        #self.x_studio_ultima_ubicacin = ''
        for record in self:
            if r.x_studio_localidad_2.id:
                if len(str(record.x_studio_localidad_2.display_name).rsplit(',',1))>=2:
                    record['x_studio_locacion_recortada'] = str(record.x_studio_localidad_2.display_name).rsplit(',',1)[1]
            """
            if record.x_studio_ultima_ubicacin:
                if (len(str(record.x_studio_ultima_ubicacin).rsplit(',',1))>=2) :
                    record['x_studio_locacion_recortada'] = str(record.x_studio_ultima_ubicacin).rsplit(',',1)[1]
            """


    x_studio_localidad = fields.Char(store=False, string='Localidad')
    x_studio_localidad_1 = fields.Many2one('res.users',string='Localidad',store=True)

    
    x_studio_localidad_2 = fields.Many2one('res.partner',string='Localidad',store=True, track_visibility='onchange')

    
    x_studio_magenta = fields.Char(readonly=True, store=True, string='Magenta', compute = '_compute_x_studio_magenta')

    @api.depends('dca')
    def _compute_x_studio_magenta(self):
        self.x_studio_magenta = ''
        for record in self:
            if len(record.dca) > 0:
                cont_color = str(record.dca[len(record.dca) - 1].porcentajeMagenta)
                record['x_studio_magenta'] = str(cont_color) 

    x_studio_magenta_anterior = fields.Char(readonly=True, store=True, string='Magenta Anterior', compute = '_compute_x_studio_magenta_anterior')

    @api.depends('dca')
    def _compute_x_studio_magenta_anterior(self):
        self.x_studio_magenta_anterior = ''
        for record in self:
            if len(record.dca) > 0:
                cont_color = str(record.dca[len(record.dca) - 2].porcentajeMagenta)
                record['x_studio_magenta_anterior'] = str(cont_color) 

    x_studio_mini = fields.Boolean(string='Mini', store=True, track_visibility='onchange')
    #x_studio_ml)
    x_studio_modelo_equipo = fields.Char(readonly=True, store=False, string='Modelo Equipo', related='product_id.name')
    
    x_studio_move_line = fields.One2many('stock.move.line','lot_id', string='Movimientos')

    
    x_studio_negro = fields.Char(store=False, string='Negro', compute = '_compute_x_studio_negro')

    @api.depends('dca')
    def _compute_x_studio_negro(self):
        self.x_studio_negro = ''
        for record in self:
            if len(record.dca) > 0:
                cont_color = str(record.dca[len(record.dca) - 1].porcentajeNegro)
                record['x_studio_negro'] = str(cont_color) 

    x_studio_negro_anterior = fields.Char(readonly=True, store=False, string='Negro Anterior', compute = '_compute_x_studio_negro_anterior')

    @api.depends('dca')
    def _compute_x_studio_negro_anterior(self):
        self.x_studio_negro_anterior = ''
        for record in self:
            if len(record.dca) > 0:
                cont_color = str(record.dca[len(record.dca) - 2].porcentajeNegro)
                record['x_studio_negro_anterior'] = str(cont_color)

    x_studio_numero_de_serie = fields.Many2one('stock.production.lot',string='Numero de serie',store=True, readonly=True, related="x_studio_field_3OnO2.serie")
    x_studio_pais = fields.Char(store=False, string='País')
    x_studio_periodo = fields.Char(readonly=False, string='periodo')
    x_studio_pg_proc = fields.Integer(readonly=True, store=False, string='Pág. Proc', compute = '_compute_x_studio_pg_proc')

    @api.depends('x_studio_field_PYss4')
    def _compute_x_studio_pg_proc(self):
        self.x_studio_pg_proc = 0
        for r in self:
            r['x_studio_pg_proc']=r.x_studio_ultimalecturam-r.x_studio_lec_ant_bn

    x_studio_ultimalecturacolor = fields.Integer(readonly=True, store=False, string='ultimalecturaColor', compute = '_compute_x_studio_ultimalecturacolor')

    @api.depends('x_studio_field_PYss4')
    def _compute_x_studio_ultimalecturacolor(self):
        self.x_studio_ultimalecturacolor = 0
        for record in self:
            t=len(record.x_studio_field_PYss4)
            h=[]
            sc=[]
            d=''
            f=0
            if t > 0:
                for a in record.x_studio_field_PYss4 :
                    h.append(a.contadorColor)
                if len(h)==0:
                    f=0
                fo=len(h)  
                if fo>3:
                    f=max(h)
                    sc=h
                    sc.sort() 
                    record['x_studio_lec_ant_color']=sc[fo-2]
                if len(h)==1:
                    f=h[0]  
                record['x_studio_ultimalecturacolor'] = f
            else:
                record['x_studio_ultimalecturacolor'] = 0


    x_studio_pg_proc_color = fields.Integer(readonly=True, store=False, string='Pág. Proc. color', compute = '_compute_x_studio_pg_proc_color')

    @api.depends('x_studio_field_PYss4')
    def _compute_x_studio_pg_proc_color(self):
        self.x_studio_pg_proc_color = 0
        for r in self:
            r['x_studio_pg_proc_color']=r.x_studio_ultimalecturacolor-r.x_studio_lec_ant_color

    
    x_studio_producto_temp = fields.Many2one('product.product',string='producto temp',store=True, readonly=True, related='x_studio_field_Zi7sY')

    

    """
    x_studio_rendimiento)
    x_studio_resultado)
    x_studio_servicio_contrato)
    x_studio_servicios)
    x_studio_solicitar_tner_amarillo)
    x_studio_solicitar_tner_bn)
    x_studio_solicitar_tner_cian_1)
    x_studio_solicitar_tner_magenta)
    )
    x_studio_tamdca)
    """
    x_studio_test = fields.Char(string='test', readonly=True)
    """
    x_studio_ticketactual)
    x_studio_tickttmp)
    x_studio_tmp_char)
    x_studio_tmpint)
    x_studio_toner)
    """
    x_studio_toner_1 = fields.One2many('dcas.dcas','serie', store=True, string='Historico de toner', domain='[["fuente","=","helpdesk.ticket"]]')
    
    x_studio_toner_compatible = fields.Many2one('product.product',string='Tóner Compatible BN',store=True, copied=True)

    x_studio_reftoner = fields.Char(string="refTonerBN", readonly=True, compute="_compute_x_studio_reftoner")
    @api.depends('x_studio_toner_compatible')
    def _compute_x_studio_reftoner(self):
        self.x_studio_reftoner = ''
        for r in self :
            if r.x_studio_toner_compatible.id:
                r['x_studio_reftoner'] = str(r.x_studio_toner_compatible.name)
            else :
                r['x_studio_reftoner'] = ''

    x_studio_tner_compatible_amarrillo = fields.Many2one('product.product',string='Tóner Compatible Amarrillo',store=True, copied=True)
    x_studio_reftonera = fields.Char(string="reftonerA", readonly=True, compute="_compute_x_studio_reftonera")
    @api.depends('x_studio_tner_compatible_amarrillo')
    def _compute_x_studio_reftonera(self):
        self.x_studio_reftonera = ''
        for r in self :
            if r.x_studio_tner_compatible_amarrillo.id:
                r['x_studio_reftonera'] = str(r.x_studio_tner_compatible_amarrillo.name)
            else :
                r['x_studio_reftonera'] = ''

    x_studio_tner_compatible_magenta = fields.Many2one('product.product',string='Tóner Compatible Magenta',store=True, copied=True)
    x_studio_reftonerm = fields.Char(string="reftonerm", readonly=True, compute="_compute_x_studio_reftonerm")
    @api.depends('x_studio_tner_compatible_magenta')
    def _compute_x_studio_reftonerm(self):
        self.x_studio_reftonerm = ''
        for r in self :
            if r.x_studio_tner_compatible_magenta.id:
                r['x_studio_reftonerm'] = str(r.x_studio_tner_compatible_magenta.name)
            else :
                r['x_studio_reftonerm'] = ''

    """
    x_studio_toner_compatible_1)
    x_studio_toner_compatible_cian)
    x_studio_toner_compatible_nombre)
    x_studio_toner_compatibles)
    x_studio_ubicacin)
    """
    x_studio_ubicacion_id = fields.Integer(string='ubicacion_id', store=True)
    
    x_studio_ubicaciontest = fields.Char(string='Cliente', readonly=True, compute='_compute_x_studio_ubicaciontest')

    @api.depends('x_studio_ultma_ubicacin')
    def _compute_x_studio_ubicaciontest(self):
        self.x_studio_ubicaciontest = ''
        for record in self:
            if record.x_studio_ultma_ubicacin:
                record['x_studio_ubicaciontest'] = str(record.x_studio_ultma_ubicacin).rsplit(',',1)[0]

    """
    x_studio_ultimafuente)
    
    """
    x_studio_ultimalecturam = fields.Integer(readonly=True, string='ultimaLecturaM', compute = '_compute_x_studio_ultimalecturam')

    @api.depends('x_studio_field_PYss4')
    def _compute_x_studio_ultimalecturam(self):
        self.x_studio_ultimalecturam = 0
        self.x_studio_periodo = ''
        for record in self:
            t=len(record.x_studio_field_PYss4)
            h=[]
            s=[]
            d=''
            f=0
            index=0
            if t > 0:
                for a in record.x_studio_field_PYss4 :
                    h.append(a.contadorMono)
                if len(h)==0:
                    f=0
                if len(h)==2:
                    f=max(h)
                    s=h
                    s.sort() 
                    index = h.index(max(h))
                    record['x_studio_lec_ant_bn']=s[1]
                if len(h)>3:
                    f=max(h)
                    s=h
                    s.sort() 
                    index = h.index(max(h))
                    record['x_studio_lec_ant_bn']=s[t-2]  
                if len(h)==1:
                    f=h[0]  
                record['x_studio_ultimalecturam'] = f
                record['x_studio_periodo'] = str(record.x_studio_field_PYss4[index].x_studio_field_no6Rb)
                #record['x_studio_periodo'] = str(len(h))
            else:
                record['x_studio_ultimalecturam'] = 0
                record['x_studio_periodo'] = 'sin lecturas'

    """
    x_studio_ultimo_contador_negro_toner)
    x_studio_ultimo_contador_toner)
    """
    x_studio_ultimo_mantenimiento_preventivo = fields.Datetime(string = 'Ultimo mantenimiento preventivo', store=True)
    

    x_studio_ultma_ubicacin = fields.Char(readonly=True, string='Ultíma Ubicación', compute = '_compute_x_studio_ultma_ubicacin')

    @api.depends('x_studio_cambio')
    def _compute_x_studio_ultma_ubicacin(self):
        for r in self:
            self.x_studio_ultma_ubicacin = ''
            self.x_studio_delegacion = ''
            self.x_studio_calle = ''
            self.x_studio_cp = ''
            self.x_studio_interior = ''
            self.x_studio_exterior = ''
            self.x_studio_colonia = ''
            self.x_studio_ciudad = ''
            self.x_studio_estado_1 = ''
            self.x_studio_zona = ''
            tam=len(r.x_studio_move_line)
            pos=tam-1
            if(r.x_studio_localidad_2.id):
                loca=r.x_studio_localidad_2
                r['x_studio_ultma_ubicacin'] = str(loca.display_name)
                r['x_studio_delegacion']=str(loca.l10n_mx_edi_locality)
                r['x_studio_calle']=str(loca.street_name)
                r['x_studio_cp']=str(loca.zip)
                r['x_studio_interior']=str(loca.street_number2)
                r['x_studio_exterior']=str(loca.street_number)
                r['x_studio_colonia']=str(loca.l10n_mx_edi_colony)
                r['x_studio_ciudad']=str(loca.x_studio_ciudad)
                r['x_studio_estado_1']=str(loca.state_id.name)
                r['x_studio_zona']=str(loca.x_studio_field_SqU5B)

    
    x_studio_venta = fields.Boolean(store=True, string='Venta')
    #x_studio_w)
    x_studio_zona = fields.Char(readonly=True, string='Zona')
    #x_x_studio_equipo_por_nmero_de_serie_2__helpdesk_ticket_count)



    
    def gener_tabla_tickets(self):
      serie_name = self.mapped('name')[0]
      serie_id = self.mapped('id')[0]
      #_logger.info('serie_name: '+ str(serie_name) + ' serie_id: ' + str(serie_id))
      if serie_id:
        #_logger.info('Entreeeeeeeeeeee')
        query = 'select "helpdesk_ticket_id" from helpdesk_ticket_stock_production_lot_rel where "stock_production_lot_id" = ' + str(serie_id)
        self.env.cr.execute(query)
        resultadoQuery = self.env.cr.fetchall()
        #_logger.info('resultadoQuery: ' + str(resultadoQuery))
        dominio_tickets_odoo = [('serie', '=', serie_id), ('fuente', '=', 'helpdesk.ticket'), ('x_studio_tickett', '!=', False)]
        tickets_toner = self.env['dcas.dcas'].search(dominio_tickets_odoo) #.x_studio_tickett
        #_logger.info('tickets_toner: ' + str(tickets_toner))
        lista_tickets = []
        for id_ticket in resultadoQuery:
          lista_tickets.append(id_ticket[0])
        for id_ticket in tickets_toner:
          lista_tickets.append(id_ticket.x_studio_tickett)
        #_logger.info('lista_tickets: ' + str(lista_tickets))
        dominio_tickets_odoo = [('id', 'in', lista_tickets)]
        tickets_odoo = self.env['helpdesk.ticket'].search(dominio_tickets_odoo)
        #_logger.info('tickets_odoo: ' + str(tickets_odoo))

        #tickets techra
        #dominio_tickets_techra = [(serie_name, 'in', 'numeroDeSerieTechra')]
        tickets_techra = self.env['helpdesk.ticket.techra'].search([('numeroDeSerieTechra', 'ilike', serie_name)])
        #tickets_techra = tickets_techra.filtered(lambda x: serie_name in x.numeroDeSerieTechra )
        #_logger.info('tickets_techra: ' + str(tickets_techra))

        

        filas = """"""
        for ticket in tickets_techra:
            data_ticke = {}

            contadores = ''
            if ticket.series:
                numero_de_serie = ''
                for serie in ticket.series:
                    numero_de_serie = serie.serie.name
                    if serie.x_studio_color_o_bn == 'Color':
                        contadores = contadores + 'Serie: ' + numero_de_serie + '</br>Equipo B/N o Color: ' + str(serie.x_studio_color_o_bn) + '</br>Contador B/N anterior: ' + str(serie.x_studio_contador_mono_anterior_1) + '</br>Contador B/N actual: ' + str(serie.contadorMono) + '</br>Contador Color anterior: ' + str(serie.x_studio_contador_color_anterior) + '</br>Contador Color actual: ' + str(serie.contadorColor) + '</br>'
                    if serie.x_studio_color_o_bn == 'B/N':
                        contadores = contadores + 'Serie: ' + numero_de_serie + '</br>Equipo B/N o Color: ' + str(serie.x_studio_color_o_bn) + '</br>Contador B/N anterior: ' + str(serie.x_studio_contador_mono_anterior_1) + '</br>Contador B/N actual: ' + str(serie.contadorMono) + '</br>'

            if ticket.diagnosticos:
                diagnosticos_ticket = []
                for registro in ticket.diagnosticos:
                    info = {
                        "create_date": str(registro.fechaDiagnosticoTechra),
                        "estadoTicket": str(registro.estadoTicket),
                        "comentario": str(registro.comentario),
                        "encargado": str(registro.create_uid.name)
                    }
                    diagnosticos_ticket.append(info)
                data_ticke["diagnosticos"] = diagnosticos_ticket

            filas = filas + """
                            \n<tr>
                                <td></td>
                                <td>""" + str(ticket.numTicketDeTechra) + """</td>
                                <td>""" + str(ticket.creado_el) + """</td>
                                <td>""" + str(ticket.numeroDeSerieTechra) + """</td>
                                <td>""" + str(ticket.cliente_text) + """</td>
                                <td>""" + str(ticket.areaDeAtencionTechra) + """</td>
                                <td>""" + str(ticket.zona_de_domicilio) + """</td>
                                <td>""" + str(ticket.localidad_text) + """</td>
                                <td>""" + str(ticket.descripcionDelReporteTechra) + """</td>
                                <td>""" + str(ticket.estadoTicketTechra) + """</td>

                                <td>""" + str(contadores) + """</td>
                                
                                <td>""" + str(ticket.ultima_nota) + """</td>
                                <td>""" + str(ticket.fecha_ultima_nota) + """</td>
                                <td>""" + str(json.dumps(data_ticke)) + """</td>
                              </tr>
                          """
        for ticket in tickets_odoo:
            ultimo_diagnostico_fecha = ''
            data_ticke = {}
            if ticket.diagnosticos:
                diagnosticos_ticket = []
                for registro in ticket.diagnosticos:
                    if not registro.creadoPorSistema and registro.comentario != False:
                        ultimo_diagnostico_fecha = str(registro.create_date)
                    info = {
                        "create_date": str(registro.create_date),
                        "estadoTicket": str(registro.estadoTicket),
                        "comentario": str(registro.comentario),
                        "encargado": str(registro.create_uid.name)
                    }
                    diagnosticos_ticket.append(info)
                data_ticke["diagnosticos"] = diagnosticos_ticket

            if ticket.x_studio_tipo_de_vale != 'Requerimiento':
                filas = filas + """
                                    \n<tr>
                                        <td></td>
                                        <td><a href='https://gnsys-corp.odoo.com/web#id=""" + str(ticket.id) + """&model=helpdesk.ticket&view_type=form&menu_id=406' target='_blank'>""" + str(ticket.id) + """</a></td>
                                        <td>""" + str(ticket.create_date) + """</td>
                                        <td>""" + str(ticket.serie_y_modelo) + """</td>
                                        <td>""" + str(ticket.partner_id.name) + """</td>
                                        <td>""" + str(ticket.team_id.name) + """</td>
                                        <td>""" + str(ticket.x_studio_field_6furK) + """</td>
                                        <td>""" + str(ticket.direccionLocalidadText) + """</td>
                                        <td>""" + str(ticket.primerDiagnosticoUsuario) + """</td>
                                        <td>""" + str(ticket.stage_id.name) + """</td>
                                        <td>""" + str(ticket.contadores_anteriores) + """</td>
                                        <td>""" + str(ticket.x_studio_ultima_nota) + """</td>
                                        <td>""" + str(ultimo_diagnostico_fecha) + """</td>
                                        <td>""" + str(json.dumps(data_ticke)) + """</td>
                                    </tr>
                                """ 
            else:
                contadores = ''
                series_toner = ticket.mapped('x_studio_equipo_por_nmero_de_serie_1')
                #_logger.info('x_studio_equipo_por_nmero_de_serie_1: ' + str(series_toner))
                if series_toner:
                    for serie in series_toner:
                        numero_de_serie = serie.serie.name
                        if serie.x_studio_color_o_bn == 'Color':
                            #contadores = contadores + 'Serie: ' + numero_de_serie + 'Equipo B/N o Color: ' + str(serie.x_studio_color_o_bn) + '</br>Contador B/N anterior: ' + str(serie.x_studio_contador_mono_anterior_1) + '</br>Contador B/N actual: ' + str(serie.contadorMono) + '</br>Contador Color anterior: ' + str(serie.x_studio_contador_color_anterior) + '</br>Contador Color actual: ' + str(serie.contadorColor) + '</br>'
                            contadores = contadores + 'Serie: ' + numero_de_serie + '</br>Equipo B/N o Color: ' + str(serie.x_studio_color_o_bn) + '</br>Contador B/N actual: ' + str(serie.contadorMono) + '</br>Contador Color actual: ' + str(serie.contadorColor) + '</br>'
                        if serie.x_studio_color_o_bn == 'B/N':
                            contadores = contadores + 'Serie: ' + numero_de_serie + '</br>Equipo B/N o Color: ' + str(serie.x_studio_color_o_bn) + '</br>Contador B/N actual: ' + str(serie.contadorMono) + '</br>'


                filas = filas + """
                                    \n<tr>
                                        <td></td>
                                        <td><a href='https://gnsys-corp.odoo.com/web#id=""" + str(ticket.id) + """&model=helpdesk.ticket&view_type=form&menu_id=406' target='_blank'>""" + str(ticket.id) + """</a></td>
                                        <td>""" + str(ticket.create_date) + """</td>
                                        <td>""" + str(ticket.serie_y_modelo) + """</td>
                                        <td>""" + str(ticket.partner_id.name) + """</td>
                                        <td>""" + str(ticket.team_id.name) + """</td>
                                        <td>""" + str(ticket.x_studio_field_6furK) + """</td>
                                        <td>""" + str(ticket.direccionLocalidadText) + """</td>
                                        <td>""" + str(ticket.primerDiagnosticoUsuario) + """</td>
                                        <td>""" + str(ticket.stage_id.name) + """</td>
                                        <td>""" + str(contadores) + """</td>
                                        <td>""" + str(ticket.x_studio_ultima_nota) + """</td>
                                        <td>""" + str(ultimo_diagnostico_fecha) + """</td>
                                        <td>""" + str(json.dumps(data_ticke)) + """</td>
                                    </tr>
                                """ 


        #<th style="width:10%;">Contador B/N</th>
        #<th style="width:10%;">Contador color</th>

        tabla_3 = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    .modal-dialog {
                        max-width: 90% !important;
                    }

                </style>
            </head>
            <body>
                <div class='row'>
                    <div class='col-sm-12'>
                        <table id="table_id" class="table table-striped table-bordered" style="width:100%">
                            <thead>
                                <tr>
                                    <th></th>
                                    <th>Ticket</th>
                                    <th>Fecha</th>
                                    <th>No. Serie</th>
                                    <th>Cliente</th>
                                    <th>Área de atención</th>
                                    <th>Zona</th>
                                    <th>Ubicación</th>
                                    <th>Falla</th>
                                    <th>último estatus ticket</th>
                                    <th>Contadores</th>
                                    <th>última Nota</th>
                                    <th>Fecha nota</th>
                                    <th>DatosTicket</th>
                                </tr>
                            </thead>
                            <tbody>
                                """ + filas + """
                            </tbody>
                            <tfoot>
                                <tr>
                                    <th></th>
                                    <th>Ticket</th>
                                    <th>Fecha</th>
                                    <th>No. Serie</th>
                                    <th>Cliente</th>
                                    <th>Área de atención</th>
                                    <th>Zona</th>
                                    <th>Ubicación</th>
                                    <th>Falla</th>
                                    <th>último estatus ticket</th>
                                    <th>Contadores</th>
                                    <th>última Nota</th>
                                    <th>Fecha nota</th>
                                    <th>DatosTicket</th>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>

                <script>
                    
                    var table_id = 1
                    var hasOwnProperty = Object.prototype.hasOwnProperty;

                    function isEmpty(obj) {

                        // null and undefined are "empty"
                        if (obj == null) return true;

                        // Assume if it has a length property with a non-zero value
                        // that that property is correct.
                        if (obj.length > 0)    return false;
                        if (obj.length === 0)  return true;

                        // If it isn't an object at this point
                        // it is empty, but it can't be anything *but* empty
                        // Is it empty?  Depends on your application.
                        if (typeof obj !== "object") return true;

                        // Otherwise, does it have any properties of its own?
                        // Note that this doesn't handle
                        // toString and valueOf enumeration bugs in IE < 9
                        for (var key in obj) {
                            if (hasOwnProperty.call(obj, key)) return false;
                        }

                        return true;
                    }

                    function format ( d, id ) {
                        var data_ticket = JSON.parse( d.DatosTicket );
                        //console.log(data_ticket)
                        var diagnosticos = data_ticket.diagnosticos

                        var filas = ""

                        for (i = 0; i < diagnosticos.length; i++) {
                            filas += "<tr> <td>" + diagnosticos[i].create_date + "</td> <td>" + diagnosticos[i].estadoTicket + "</td> <td>" + diagnosticos[i].comentario + "</td> <td>" + diagnosticos[i].encargado + "</td> </tr>"
                        }
                        
                        var tabla = "<table id='table_diagnostico_" + id + "' class='table table-striped table-bordered' style='width:100%'> <thead> <tr> <th>Creado_el</th><th>Estado_de_ticket</th><th>Diagnostico</th><th>Encargado</th> </tr> </thead> <tbody> " + filas + " </tbody> <tfoot> <tr> <th>Creado_el</th><th>Estado_de_ticket</th><th>Diagnostico</th><th>Encargado</th> </tr> </tfoot> </table> "
                        
                        return tabla;
                    }

                    $(document).ready( function () {
                        try {
                            var table = $('#table_id').DataTable( {
                                dom: 'Bfrtip',
                                lengthMenu: [
                                    [ 10, 25, 50, -1 ],
                                    [ '10 filas', '25 filas', '50 filas', 'Todas las filas' ]
                                ],
                                buttons: [
                                    'pageLength',
                                    'copyHtml5',
                                    'excelHtml5',
                                    'csvHtml5',
                                    'pdfHtml5'
                                ],
                                "language": {
                                    "lengthMenu": "Mostrar _MENU_ registros por página",
                                    "zeroRecords": "Sin registros - perdón =(",
                                    "info": "Página _PAGE_ de _PAGES_",
                                    "infoEmpty": "No hay registros disponibles",
                                    "infoFiltered": "(Filtrado de _MAX_ registros)",
                                    "search": "Buscar",
                                    "Previous": "Anterior",
                                    "Next": "Siguiente"
                                },
                                "scrollX": true,
                                scrollY: '50vh',
                                scrollCollapse: true,
                                "columnDefs": [
                                    {
                                        "targets": [ 13 ],
                                        "visible": false,
                                        "searchable": true
                                    }
                                ],
                                "columns": [
                                    {
                                        "class":          "details-control",
                                        "orderable":      false,
                                        "data":           null,
                                        "defaultContent": '<i class="fa fa-info-circle" aria-hidden="false"> </ i>'
                                    },
                                    { "data": "Ticket" },
                                    { "data": "Fecha" },
                                    { "data": "No. Serie" },
                                    { "data": "Cliente" },
                                    { "data": "Área de atención" },
                                    { "data": "Zona" },
                                    { "data": "Ubicación" },
                                    { "data": "Falla" },
                                    { "data": "último estatus ticket" },
                                    { "data": "Contadores" },
                                    { "data": "última Nota" },
                                    { "data": "Fecha nota" },
                                    { "data": "DatosTicket" }
                                ],
                                "order": [[2, 'desc']],
                                colReorder: true
                            } );

                            var detailRows = [];

                            $('#table_id tbody').on( 'click', 'tr td.details-control', function () {
                                var tr = $(this).closest('tr');
                                var row = table.row( tr );
                                var idx = $.inArray( tr.attr('id'), detailRows );
                                
                                var data_ticket_c = JSON.parse( row.data().DatosTicket );
                                //console.log(isEmpty(data_ticket_c))
                                if ( !isEmpty( data_ticket_c ) ) {

                                    if ( row.child.isShown() ) {
                                        tr.removeClass( 'details' );
                                        row.child.hide();
                             
                                        // Remove from the 'open' array
                                        detailRows.splice( idx, 1 );

                                    } else {
                                        tr.addClass( 'details' );
                                        row.child( format( row.data(), table_id ) ).show();
                                        

                                        //table_diagnostico
                                        //var table_diagnostico = $('table.display').DataTable( {
                                        //var table_diagnostico = row.child.DataTable( {
                                        var table_diagnostico = $('#table_diagnostico_' + table_id).DataTable( {
                                            dom: 'Bfrtip',
                                            lengthMenu: [
                                                [ 10, 25, 50, -1 ],
                                                [ '10 filas', '25 filas', '50 filas', 'Todas las filas' ]
                                            ],
                                            buttons: [
                                                'pageLength',
                                                'copyHtml5',
                                                'excelHtml5',
                                                'csvHtml5',
                                                'pdfHtml5'
                                            ],
                                            "language": {
                                                "lengthMenu": "Mostrar _MENU_ registros por página",
                                                "zeroRecords": "Sin registros - perdón =(",
                                                "info": "Página _PAGE_ de _PAGES_",
                                                "infoEmpty": "No hay registros disponibles",
                                                "infoFiltered": "(Filtrado de _MAX_ registros)",
                                                "search": "Buscar",
                                                "Previous": "Anterior",
                                                "Next": "Siguiente"
                                            },
                                            "columns": [
                                                { "data": "Creado_el" },
                                                { "data": "Estado_de_ticket" },
                                                { "data": "Diagnostico" },
                                                { "data": "Encargado" }
                                            ],
                                            "order": [[0, 'asc']],
                                            colReorder: true
                                        } );


                                        table_id += 1


                                        // Add to the 'open' array
                                        if ( idx === -1 ) {
                                            detailRows.push( tr.attr('id') );
                                        }
                                    }
                                } else {
                                    alert("No se cuentan con diagnosticos en el ticket seleccionado")
                                }
                            } );
                        } catch (error) {
                            console.error("error");
                            console.error(error);
                        }
                    } );

                </script>

            </body>
            </html>
        """        

        self.html = tabla_3


    
    
    
class contadores_lines(models.Model):
    _name="cambios.localidad"
    _description = "Cambios de Localidad"
    estado=fields.Selection(selection=[('1','Por Confirma'),('2','Confirmado')])
    serie=fields.Many2one('stock.production.lot')
    origen=fields.Many2one('res.partner')
    destino=fields.Many2one('res.partner')
    contrato1=fields.Many2one('contrato')
    servicio1=fields.Many2one('servicios')
    tipo=fields.Selection(selection=[('1','Ubicacion'),('2','servicios'),('3','Ambos')])
    nota=fields.Char()


    @api.onchange('serie')
    def ubicacion(self):
        m=self.serie.x_studio_localidad_2
        if(m):
           self.origen=m.id
                    
                    
    def cambio(self):
        if(self.servicio1 and (self.tipo=='2' or self.tipo=='3')):
            self.serie.servicio=self.servicio1.id
            self.estado='2'
        if(self.destino and (self.tipo=='1' or self.tipo=='3')):
            origen2=self.env['stock.warehouse'].search([('x_studio_field_E0H1Z','=',self.origen.id)])
            destino2=self.env['stock.warehouse'].search([('x_studio_field_E0H1Z','=',self.destino.id)])
            self.env['stock.move.line'].create({'product_id':self.serie.product_id.id, 'product_uom_id':1,'location_id':origen2.lot_stock_id.id if(origen2.lot_stock_id.id) else 12,'product_uom_qty':1,'lot_id':self.serie.id
                                                ,'date':datetime.datetime.now(),'location_dest_id':destino2.lot_stock_id.id})
            destino2.lot_stock_id.write({'x_studio_field_JoD2k':destino2.id})
            self.serie.write({'x_studio_cliente':self.destino.parent_id.id,'x_studio_localidad_2':self.destino.id})
            self.serie.x_studio_cambio = not self.serie.x_studio_cambio
            self.estado='2'

            
            
