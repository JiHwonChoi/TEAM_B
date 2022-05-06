#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import psycopg2
import cv2
from config import DB
from cloud_utils import Cloud

class Database:
    def __init__(self):
        self.db = psycopg2.connect(host=DB['host'],
                                dbname=DB['dbname'],
                                user=DB['user'],
                                password = DB['password'],
                                port=DB['port'])
        self.cursor = self.db.cursor()

        self.cloud = Cloud()
        self.map = self.get_map()


    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

        if query.startswith('S'):
            row = self.cursor.fetchall()
            return row

        else:
            self.db.commit()


    def image_upload(self, image):
        res = self.cloud.upload_image(image)
        return res

    def get_map(self):
        img = cv2.imread('map.pgm')
        return img

if __name__=="__main__":
    db = Database()
    cv2.imshow("map test", db.map)
    cv2.waitKey(0)