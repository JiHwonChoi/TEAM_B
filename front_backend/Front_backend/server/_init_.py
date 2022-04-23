from flask import Flask
from flask_cors import CORS
from server.routes import config

## app 만들기

app = Flask(__name__)

## config

app.config.from_object(config)

## CORS 설정
CORS(app)

from server.routes import route