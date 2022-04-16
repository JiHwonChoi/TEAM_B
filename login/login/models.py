
import os
import sys
import psycopg2

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from config import DB
db = psycopg2.connect(host=DB['host'],
    dbname=DB['dbname'],
    user=DB['user'],
    password = DB['password'],
    port=DB['port'])

print(db)