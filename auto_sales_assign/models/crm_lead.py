from odoo import fields, models, api
from datetime import date, datetime, timedelta
import datetime
from odoo.exceptions import ValidationError, UserError

import logging


class CrmPlatform(models.Model):
    _name = 'crm.platform'

    name = fields.Char()

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    destination = fields.Char()
    travel_date = fields.Datetime()
    platform = fields.Many2one('crm.platform')

    # @api.model
    def action_assign_leads(self):
        for rec in self:
            # self.ensure_one()
        # This calls the existing method from res.config.settings
            return rec.env['res.config.settings'].action_crm_assign_leads()

    def open_whatsapp_web(self):
        if len(self.phone) <= 11:
            if self.phone:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://wa.me/+2{}'.format(self.phone),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))
        else:
            if self.phone:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://wa.me/{}'.format(self.phone),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))


    def open_whatsapp_mobile(self):
        if len(self.phone) <= 11:
            if self.phone:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://api.whatsapp.com/send/?phone=+2{}'.format(self.phone),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))
        else:
            if self.phone:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://api.whatsapp.com/send/?phone={}'.format(self.phone),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))
