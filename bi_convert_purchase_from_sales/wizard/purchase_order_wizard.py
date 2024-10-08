# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime


class PurchaseOrderExtension(models.Model):
    _inherit = 'purchase.order'

    sale_id = fields.Many2one(
        'sale.order', string='Sale Order',
        help='Link to the related sale order.')

    sale_order_template_id = fields.Many2one(
        'sale.order.template',
        help='Link to the related sale order template.')


class CreatePurchaseOrder(models.TransientModel):
    _name = 'create.purchaseorder'
    _description = "Create Purchase Order"

    new_order_line_ids = fields.One2many('getsale.orderdata', 'new_order_line_id', string="Order Line")
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True)
    date_order = fields.Datetime(string='Order Date', required=True, copy=False, default=fields.Datetime.now)
    analytic_distribution = fields.Json()
    cost = fields.Float()
    pnr = fields.Char(string="PNR")
    customer_name = fields.Char(string='Name')
    airline = fields.Char()
    serial_number = fields.Char()
    route = fields.Char()
    tkt_no = fields.Char()
    reference = fields.Char()
    price = fields.Float()

    @api.model
    def default_get(self, default_fields):
        res = super(CreatePurchaseOrder, self).default_get(default_fields)
        data = self.env['sale.order'].browse(self._context.get('active_ids', []))
        update = []
        for line in data.order_line:
            update.append((0, 0, {
                'product_id': line.product_id.id,
                'product_uom': line.product_uom.id,
                'order_id': line.order_id.id,
                'name': line.name,
                'analytic_distribution': line.analytic_distribution,
                'product_qty': line.product_uom_qty,
                'price_unit': line.cost,
                'product_subtotal': line.price_subtotal,
                'customer_name': line.customer_name,
                'pnr': line.pnr,
                'airline': line.airline,
                'serial_number': line.serial_number,
                'route': line.route,
                'tkt_no': line.tkt_no,
                'reference': line.reference,
                'price': line.price_unit,
            }))
            # print(record.cost,'[[[[[[[[[[[')
        res.update({'new_order_line_ids': update})
        return res

    def action_create_purchase_order(self):
        self.ensure_one()
        res = self.env['purchase.order'].browse(self._context.get('id',[]))
        value = []
        so = self.env['sale.order'].browse(self._context.get('active_id'))
        pricelist = self.partner_id.property_product_pricelist
        partner_pricelist = self.partner_id.property_product_pricelist
        sale_order_name = so.name
        for data in self.new_order_line_ids:
            sale_order_name = data.order_id.name
            if not sale_order_name:
                sale_order_name = so.name
            # if partner_pricelist:
            #     product_context = dict(self.env.context, partner_id=self.partner_id.id, date=self.date_order,
            #                            uom=data.product_uom.id)
            #     final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(
            #         data.product_id, data.product_qty or 1.0, self.partner_id)
            #
            # else:
            #     final_price = data.product_id.standard_price
            value.append([0, 0, {
                'product_id': data.product_id.id,
                'name': data.name,
                'product_qty': data.product_qty,
                'analytic_distribution': data.analytic_distribution,
                'order_id': data.order_id.id,
                'taxes_id': data.product_id.supplier_taxes_id.ids,
                'date_planned': data.date_planned,
                'price_unit': data.price_unit,
                'customer_name': data.customer_name,
                'pnr': data.pnr,
                'airline': data.airline,
                'serial_number': data.serial_number,
                'route': data.route,
                'tkt_no': data.tkt_no,
                'reference': data.reference,
                'price': data.price_unit,

            }])
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.partner_id.id,
            'date_order': str(self.date_order),
            'order_line': value,
            'origin': sale_order_name,
            'partner_ref': sale_order_name,
            'sale_id': so.id,
            'sale_order_template_id': so.sale_order_template_id.id
        })
        sale_order = self.env['sale.order'].browse(self._context.get('active_ids', []))
        message = purchase_order.name + ' has been created by ' + self.env.user.name
        sale_order.message_post(body=message)

        return res


class Getsaleorderdata(models.TransientModel):
    _name = 'getsale.orderdata'
    _description = "Get Sale Order Data"

    new_order_line_id = fields.Many2one('create.purchaseorder')

    product_id = fields.Many2one('product.product', string="Product", required=True)
    name = fields.Char(string="Description")
    product_qty = fields.Float(string='Quantity', required=True)
    date_planned = fields.Datetime(string='Scheduled Date', default=datetime.today())
    product_uom = fields.Many2one('uom.uom', string='Product Unit of Measure')
    order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', index=True)
    price_unit = fields.Float(string='Unit Price', digits='Product Price')
    product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')
    analytic_distribution = fields.Json()
    cost = fields.Float()
    pnr = fields.Char(string="PNR")
    customer_name = fields.Char(string='Name')
    airline = fields.Char()
    serial_number = fields.Char()
    route = fields.Char()
    tkt_no = fields.Char()
    reference = fields.Char()
    price = fields.Float()

    @api.depends('product_qty', 'price_unit')
    def _compute_total(self):
        for record in self:
            record.product_subtotal = record.product_qty * record.price_unit
