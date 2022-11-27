from flask import Flask
import pytest
from app import config as config_module
from app.presentation import api

config = config_module.get_config()
async_mode = None

app=Flask(__name__)
app.config.from_object(config)

@pytest.fixture(scope="module")
def create_api():
    return api.create_api(app)