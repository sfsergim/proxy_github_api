# -*- coding: utf-8 -*-
from app.data_source import models
import json


class ValidateJson(object):

    @classmethod
    def autenticate_user_with_email(cls, credentials):
        try:
            email = credentials['user_name']
            password = 'pass'

            models.User.filter_avaliable_users(email, password=None)
            return True
        except Exception as ex:
            return False

    @classmethod
    def validate_user_json(cls, credentials):
        try:    
            return json.dumps(credentials)
        except Exception as ex:
            return False

 

    