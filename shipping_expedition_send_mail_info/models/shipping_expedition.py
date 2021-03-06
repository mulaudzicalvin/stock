# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, exceptions, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class ShippingExpedition(models.Model):
    _inherit = 'shipping.expedition'
    
    date_send_mail_info = fields.Datetime(
        string='Fecha email info' 
    )
    
    @api.one
    def action_send_mail_info_real(self):
        _logger.info('Enviamos el email respecto a la expedicion ' + str(self.id))
        mail_compose_message_vals = {                    
            'author_id': self.user_id.partner_id.id,
            'record_name': self.name,                                                                                                                                                                                           
        }
        mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo().create(mail_compose_message_vals)
        return_onchange_template_id = mail_compose_message_obj.onchange_template_id(self.carrier_id.mail_info_mail_template_id.id, 'comment', 'shipping.expedition', self.id)                                
        
        mail_compose_message_obj.update({
            'author_id': mail_compose_message_vals['author_id'],
            'template_id': self.carrier_id.mail_info_mail_template_id.id,
            'composition_mode': 'comment',
            'model': 'shipping.expedition',
            'res_id': self.id,
            'body': return_onchange_template_id['value']['body'],
            'subject': return_onchange_template_id['value']['subject'],
            'email_from': return_onchange_template_id['value']['email_from'],
            'partner_ids': return_onchange_template_id['value']['partner_ids'],
            #'attachment_ids': return_onchange_template_id['value']['attachment_ids'],
            'record_name': mail_compose_message_vals['record_name'],
            'no_auto_thread': False,                     
        })                                         
        mail_compose_message_obj.send_mail_action()                                                        
        self.date_send_mail_info = datetime.today()        
    
    @api.one
    def action_send_mail_info(self):
        allow_send = False
        if self.carrier_id.send_mail_info == True:
            if self.carrier_id.mail_info_mail_template_id.id > 0:
                if self.date_send_mail_info == False:
                    if self.state not in ['error', 'generate', 'canceled', 'delivered', 'incidence']:
                        if self.partner_id.email != False:
                            if self.carrier_id.carrier_type == 'nacex':
                                allow_send = True
                            else:
                                if self.delegation_name != False and self.delegation_phone != False:
                                    allow_send = True
                            # allow_send
                            if allow_send == True:
                                self.action_send_mail_info_real()
            
    @api.model    
    def cron_shipping_expeditionsend_mail_info(self):
        # not nacex
        shipping_expedition_ids = self.env['shipping.expedition'].search(
            [
                ('carrier_id.carrier_type', '!=', 'nacex'),
                ('carrier_id.send_mail_info', '=', True),
                ('carrier_id.mail_info_mail_template_id', '!=', False),
                ('state', 'not in', ('error', 'generate', 'canceled', 'delivered', 'incidence')),
                ('user_id', '!=', False),
                ('date_send_mail_info', '=', False),
                ('delegation_name', '!=', False),
                ('delegation_phone', '!=', False),
                ('partner_id.email', '!=', False),
                ('picking_id.date_done', '!=', False)
            ]
        )
        if len(shipping_expedition_ids) > 0:
            for shipping_expedition_id in shipping_expedition_ids:
                shipping_expedition_id.action_send_mail_info()
        # nacex
        shipping_expedition_ids = self.env['shipping.expedition'].search(
            [
                ('carrier_id.carrier_type', '=', 'nacex'),
                ('carrier_id.send_mail_info', '=', True),
                ('carrier_id.mail_info_mail_template_id', '!=', False),
                ('state', 'not in', ('error', 'generate', 'canceled', 'delivered', 'incidence')),
                ('user_id', '!=', False),
                ('date_send_mail_info', '=', False),
                ('partner_id.email', '!=', False),
                ('picking_id.date_done', '!=', False)
            ]
        )
        if len(shipping_expedition_ids) > 0:
            for shipping_expedition_id in shipping_expedition_ids:
                shipping_expedition_id.action_send_mail_info()