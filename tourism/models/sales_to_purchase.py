from odoo import fields, models, api, _


class SaleOrderLineSearch(models.Model):
    _inherit = 'purchase.order.line'

    pnr = fields.Char(string="PNR")
    customer_name = fields.Char(string='Name')
    # pnr = fields.Char()
    airline = fields.Char()
    serial_number = fields.Char()
    route = fields.Char()
    tkt_no = fields.Char()
    reference = fields.Char()
    price = fields.Float()
