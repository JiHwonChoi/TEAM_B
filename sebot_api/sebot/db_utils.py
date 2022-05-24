#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import json
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

        if query.startswith('S') or query.startswith('s'):
            row = self.cursor.fetchall()
            return row

        else:
            self.db.commit()


    def image_upload(self, image, user_idx, point):
        res = self.cloud.upload_image(image)
        print(res)
        if res[1]:
            query = 'INSERT INTO emergency ("file_name", "user_idx", "location") VALUES (%s, %s, %s)'
            self.execute(query, (res[0], user_idx, point))
        return res[1]


    def get_map(self):
        img = cv2.imread('hospital.pgm')
        return img

    
    def get_image_info(self, idx):
        image_query = 'SELECT e.file_name, mem.user_name, e.location FROM emergency AS e INNER JOIN member_info AS mem ON mem.idx = e.user_idx WHERE e.idx = %s'
        query_res = self.execute(image_query, (idx,))
        url = self.cloud.get_image(query_res[0][0])
        res = {}
        res['url'] = url
        res['time'] = query_res[0][0]
        res['name'] = query_res[0][1]
        res['location'] = query_res[0][2]
        return res
    
    def get_map_location(self, idx):
        point_query = 'SELECT map_point FROM map_info WHERE idx = 1'
        json_dict = self.execute(point_query)[0][0]

        target_point = json_dict[str(idx)]
        return target_point['x'], target_point['y']





if __name__=="__main__":
    db = Database()
    
    # cv2.imshow("map test", db.map)
    # cv2.waitKey(0)