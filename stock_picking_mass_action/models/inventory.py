from odoo import _, fields, api
from odoo.models import Model
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
import logging, ast
_logger = logging.getLogger(__name__)
import threading
class StockPicking(Model):
    _inherit = 'stock.inventory'    

    def _action_done(self):
        negative = next((line for line in self.mapped('line_ids') if line.product_qty < 0 and line.product_qty != line.theoretical_qty), False)
        if negative:
            raise UserError(_('You cannot set a negative product quantity in an inventory line:\n\t%s - qty: %s') % (negative.product_id.name, negative.product_qty))
        threaded_calculation = threading.Thread(target=self.action_check(), args=())
        self.write({'state': 'done'})
        threaded_post = threading.Thread(target=self.post_inventory(), args=())
        for r in self.mapped('line_ids'):
            if(r.x_studio_field_yVDjd):
                i=self.env['stock.quant'].search([['product_id','=',r.product_id.id],['location_id','=',r.location_id.id]])
                i.sudo().write({'x_studio_field_kUc4x':r.x_studio_field_yVDjd.id})
        return True

class StockPickingLocation(Model):
    _inherit = 'stock.inventory.line'
    x_studio_field_yVDjd=fields.Many2one(string='Ubicación del Inventario' 'x_ubicacion_inventario')

class LocationStock(Model):
    _name='x_ubicacion_inventario'
    x_name=fields.Char()
    

class StockPic(Model):
    _inherit = 'stock.move'
    def _action_confirm(self, merge=True, merge_into=False):
        """ Confirms stock move or put it in waiting if it's linked to another move.
        :param: merge: According to this boolean, a newly confirmed move will be merged
        in another move of the same picking sharing its characteristics.
        """
        move_create_proc = self.env['stock.move']
        move_to_confirm = self.env['stock.move']
        move_waiting = self.env['stock.move']

        to_assign = {}
        for move in self:
            if move.state != 'draft':
                continue
            # if the move is preceeded, then it's waiting (if preceeding move is done, then action_assign has been called already and its state is already available)
            if move.move_orig_ids:
                move_waiting |= move
            else:
                if move.procure_method == 'make_to_order':
                    move_create_proc |= move
                else:
                    move_to_confirm |= move
            if move._should_be_assigned():
                key = (move.group_id.id, move.location_id.id, move.location_dest_id.id)
                if key not in to_assign:
                    to_assign[key] = self.env['stock.move']
                to_assign[key] |= move

        # create procurements for make to order moves
        procurement_requests = []
        for move in move_create_proc:
            values = move._prepare_procurement_values()
            origin = (move.group_id and move.group_id.name or (move.origin or move.picking_id.name or "/"))
            procurement_requests.append(self.env['procurement.group'].Procurement(
                move.product_id, move.product_uom_qty, move.product_uom,
                move.location_id, move.rule_id and move.rule_id.name or "/",
                origin, move.company_id, values))
        self.env['procurement.group'].run(procurement_requests, raise_user_error=not self.env.context.get('from_orderpoint'))

        move_to_confirm.write({'state': 'confirmed'})
        (move_waiting | move_create_proc).write({'state': 'waiting'})

        # assign picking in batch for all confirmed move that share the same details
        for moves in to_assign.values():
            moves._assign_picking()
        self._push_apply()
        self._check_company()
        moves = self
        #if merge:
        #    moves = self._merge_moves(merge_into=merge_into)
        # call `_action_assign` on every confirmed move which location_id bypasses the reservation
        moves.filtered(lambda move: not move.picking_id.immediate_transfer and move._should_bypass_reservation() and move.state == 'confirmed')._action_assign()
        return moves



class StockWarehouse(Model):
    _inherit = 'stock.warehouse'

    x_studio_cliente = fields.Boolean(string = 'Cliente')
    x_studio_almacn_padre = fields.Many2one('stock.warehouse', string = 'Almacén Padre')
    x_studio_arreglo = fields.Char(string = 'arreglo')
    x_studio_field_CQyVe = fields.Many2many('res.users', store=True, string = 'Usuarios')
    x_studio_field_E0H1Z = fields.Many2one('res.partner', string = 'Ubicación')
    x_studio_mini = fields.Boolean(string = 'Mini')
    x_studio_techra = fields.Char(string = 'techra')
    x_studio_tfs = fields.Many2one('res.partner', string = 'Tfs')
    x_studio_field_E0H1Z = fields.Many2one('res.partner', string = 'Ubicación', store=True)



class StockMoveLine(Model):
    _inherit = 'stock.location'

    x_studio_field_JoD2k = fields.Many2one('stock.warehouse', string = 'Almacén', store=True)
    x_studio_almacn_padre= fields.Many2one('stock.warehouse', string = 'Almacén Padre', store=True)

class StockMoveLine(Model):
    _inherit = 'stock.move.line'
    x_studio_arreglo=fields.Char()
    x_studio_almacen = fields.Char(related='location_id.x_studio_field_JoD2k.display_name', string='Almacen')
    x_studio_field_aVMhn=fields.Many2one(related='product_id.categ_id')
    x_studio_field_3lDS0=fields.Many2one('stock.warehouse',compute='alma')
    x_studio_comentarios=fields.Text()
    x_studio_ticket=fields.Char()
    x_studio_orden_de_venta=fields.Char()
    x_studio_field_y5FBs=fields.Integer(default=0)
    x_studio_serie_destino_1=fields.Char()
    x_studio_modelo_equipo=fields.Char()
    x_studio_estado_destino=fields.Char()
    x_studio_colonia_destino=fields.Char()
    x_studio_coment=fields.Char()
    @api.depends('location_id','write_date')
    def alma(self):
        valor=False
        for r in self:
            if(r.location_id):
                if(r.location_id.x_studio_field_JoD2k):
                  valor=r.location_id.x_studio_field_JoD2k.id
        self.x_studio_field_3lDS0=valor