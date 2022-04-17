#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import sys
from datetime import datetime
import boto3

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from TEAM_B.login.login.config import CLOUD

class Cloud:
    def __init__(self):
        self.s3 = boto3.client('s3',
                    aws_access_key_id = CLOUD['AWS_ACCESS_KEY'],
                    aws_secret_access_key = CLOUD['AWS_SECRET_KEY'])


    def upload_image(self, image):
        try:
            self.s3.put_object(
                Bucket = CLOUD['BUCKET_NAME'],
                Body = image,
                Key = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S:%06m")}.jpg',
                ContentType = 'image/jpeg'
            )
            return True

        except:
            return False

