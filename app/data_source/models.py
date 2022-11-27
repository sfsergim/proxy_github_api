# -*- coding: utf-8 -*-
import datetime
import unicodedata
import app.data_source.database

from app import config as config_module
from app.domain.service import exceptions

logged_user = None
db = app.data_source.database.AppRepository.db
config = config_module.get_config()


class AbstractModel(object):
    class AlreadyExist(Exception):
        pass

    class NotExist(Exception):
        pass

    class RepositoryError(Exception):
        pass

class User(AbstractModel):
    __tablename__ = 'User'
   

    @classmethod
    def filter_users(cls):
        return cls.query.all()

    @classmethod
    def filter_avaliable_users(cls, email, password):
        # Here trying get credentials data from user in data base .
        # cls.query.filter_by(email=email, password=password)

        return True
    
    def create_from_json(cls, json_data):
        # Here validate JSON reciver from GitHub, 
        return True