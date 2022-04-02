#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import sys
import psycopg2

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from config import DB

class Database:
    def __init__(self):
        self.db = psycopg2.connect(host=DB['host'],
                                dbname=DB['dbname'],
                                user=DB['user'],
                                password = DB['password'],
                                port=DB['port'])
        self.cursor = self.db.cursor()

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