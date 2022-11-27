import os
from flask import Flask, Response
from app import config as config_module
from app.presentation import api

config = config_module.get_config()
async_mode = None

app=Flask(__name__)
app.config.from_object(config)

api.create_api(app)

def run():
        app.run(host='0.0.0.0', port=int(os.environ.get('PORTA', 10999)),debug=True)