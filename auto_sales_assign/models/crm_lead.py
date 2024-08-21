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

    destination = fields.Char(tracking=True)
    moderator = fields.Html(tracking=True)
    travel_date = fields.Datetime(tracking=True)
    return_date = fields.Datetime(tracking=True)
    platform = fields.Many2one('crm.platform', tracking=True)

    passport_number = fields.Char(string="Passport Number", tracking=True)
    birth_date = fields.Date(string="Date of Birth", tracking=True)
    gender = fields.Selection([('M', 'Male'), ('F', 'Female')], string="Gender", tracking=True)
    expiration_date = fields.Date(string="Expiration Date", tracking=True)
    passport_info = fields.Char(string="Passport Info", compute="_compute_passport_info")

    @api.depends('passport_number', 'birth_date', 'gender', 'expiration_date')
    def _compute_passport_info(self):
        for record in self:
            birth_date = record.birth_date.strftime('%d%b%y').lower() if record.birth_date else ''
            expiration_date = record.expiration_date.strftime('%d%b%y').lower() if record.expiration_date else ''
            gender = record.gender[0] if record.gender else ''
            record.passport_info = f"{record.passport_number}-{birth_date}-{gender}-{expiration_date}"

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
