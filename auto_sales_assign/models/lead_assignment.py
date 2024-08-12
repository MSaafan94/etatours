from odoo import fields, models, api, _


class SaleOrderLineSearch(models.Model):
    _name = 'crm.lead.assignment'

    sale_team = fields.Integer()
