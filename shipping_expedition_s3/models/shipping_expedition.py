# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, exceptions, fields, models

import logging
_logger = logging.getLogger(__name__)

import os
import boto3
from botocore.exceptions import ClientError

class ShippingExpedition(models.Model):
    _inherit = 'shipping.expedition'        
            
    @api.model
    def create(self, values):                            
        #create            
        return_object = super(ShippingExpedition, self).create(values)
        #operations
        if return_object.carrier_id.s3_upload==True:            
            return_object.upload_file_to_s3()
        #return                      
        return return_object
        
    @api.one
    def upload_file_to_s3(self):
        if self.carrier_id.s3_upload == True:
            # open file for reading
            picking_name_replace = self.picking_id.name.replace("/", "-")
            file_name_real = str(picking_name_replace) + '.txt'
            # folder_name
            folder_name = str(os.path.abspath(__file__))
            folder_name = folder_name.replace('_s3/models/shipping_expedition.py','_' + str(self.carrier_id.carrier_type) + '/' + str(self.carrier_id.carrier_type))
            file_name_final = str(folder_name) + '/' + str(file_name_real)
            # check if exists line
            if os.path.isfile(file_name_final):
                destination_filename = str(self.carrier_id.s3_folder) + str(file_name_real)
                # define S3
                url_s3 = False
                AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')
                AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
                AWS_REGION_NAME = tools.config.get('aws_region_name')
                AWS_BUCKET_NAME = self.carrier_id.s3_bucket
                # define
                upload_to_s3 = False
                # client
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION_NAME
                )
                try:
                    with open(file_name_final, "rb") as f:
                        s3_client.upload_fileobj(f, AWS_BUCKET_NAME, destination_filename)
                        upload_to_s3 = True
                except ClientError as e:
                    _logger.info(e)
                    upload_to_s3 = False
                    # operatons
                if upload_to_s3 == True:
                    os.remove(source_path)
                    # return_url_s3
                    url_s3 = "https://s3-" + str(AWS_REGION_NAME) + ".amazonaws.com/%s/%s" % (
                    AWS_BUCKET_NAME, destination_filename)
                else:
                    _logger.info("Error al copiar el archivo en S3")
            else:
                _logger.info("MUY RARO, el archivo no existe ("+str(file_name_final)+')')