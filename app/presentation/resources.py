# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps
import re
from copy import copy
from flask import request, g
from flask_restful import Resource
import requests, json
from app import config as config_module
from app.domain.service.authentication import ValidateJson

config = config_module.get_config()

def snake_to_camel(name):
    result = []
    for index, part in enumerate(name.split('_')):
        if index == 0:
            result.append(part.lower())
        else:
            result.append(part.capitalize())
    return ''.join(result)

class ResourceBase(Resource):
    http_methods_allowed = ['GET', 'POST', 'PUT', 'DELETE']
    entity_class = None
    me_profile = None

    def __init__(self):
        if self.logged_user is None:
            return
        self.me_profile = "LOGIN IN AND RETURN TRUE OR FALSE"

    @property
    def logged_user(self):
        return getattr(g, 'user', None)

    @staticmethod
    def camel_to_snake(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def transform_key(self, data, method):
        if isinstance(data, dict):
            return {method(key): self.transform_key(value, method) for key, value in data.items()}
        if isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, dict):
                    data[index] = {method(key): self.transform_key(value, method) for key, value in item.items()}
        return data

    @property
    def payload(self):
        payload = {}
        if request.view_args:
            payload.update(self.transform_key(request.view_args, self.camel_to_snake))
            return payload
        if request.form:
            payload.update(self.transform_key(request.form, self.camel_to_snake))
            return payload
        if request.json:
            payload.update(self.transform_key(request.json, self.camel_to_snake))
            return payload

    @property
    def payload_batch(self):
        payload = {}
        payload_list = []
        if request.method != 'GET' and request.json:
            if isinstance(request.json, list):
                for item in request.json:
                    payload.update(self.transform_key(item, self.camel_to_snake))
                    copy_json = copy(payload)
                    payload_list.append(copy_json)
                return payload_list
            payload.update(self.transform_key(request.json, self.camel_to_snake))
        if request.form:
            payload.update(self.transform_key(request.form, self.camel_to_snake))
        if request.args:
            payload.update(self.transform_key(request.args, self.camel_to_snake))
        if request.view_args:
            payload.update(self.transform_key(request.view_args, self.camel_to_snake))
        return payload


    @property
    def options(self, *args, **kwargs):
        return {'result': True}

    def response(self, data_dict):
        return {snake_to_camel(key): value for key, value in data_dict.iteritems()}

    def return_ok(self, **extra):
        result = {'result': 'OK'}
        if extra is not None:
            result.update(extra)
        return result

    def return_not_found(self, exception=None):
        return {'result': 'error', 'error': 'Not Found', 'exception': str(exception)}, 404

    def return_unexpected_error(self, exception=None):
        return {'result': 'error', 'error': 'General Error', 'exception': str(exception)}, 500

    def return_bad_request(self, exception=None):
        return {'result': 'error', 'error': 'Bad Request', 'exception': str(exception)}, 400

class UserLoginResource(ResourceBase):
    http_methods_allowed = ['GET', 'POST']

    def get(self, user_name=None):
        try:
            authenticated = ValidateJson.autenticate_user_with_email(self.payload_batch)
            if authenticated:
                g.email = self.payload_batch.get('user_name')
                return self.return_ok()
            return self.return_not_found()

        except Exception as ex:
            return self.return_unexpected_error(ex)

class Users(ResourceBase):
    http_methods_allowed = ['GET', 'POST']

    def get(self, users=None):
        try:
            url = config.URL_GITHUB+'?since={page}'.format(page=self.payload_batch['page'] )
            response = json.loads(requests.get(url).content)
            nextpage = response[-1]['id']
            lst_Users={'next_url: ':[], 'user:' : []}
            lst_Users['next_url: '].append(
                {
                'next_page:':
                'http://127.0.0.1:5324/api/github/users/since?page={nextpage}'.format(nextpage = nextpage)
                }
            )

            for i in response:
                lst_Users['user:'].append(
                    i
                )

            authenticated = ValidateJson.validate_user_json(lst_Users)
            if authenticated:
                return lst_Users
            return self.return_not_found()
        except Exception as ex:
            return self.return_unexpected_error(ex)

class UserDetails(ResourceBase):
    http_methods_allowed = ['GET', 'POST']

    def get(self, user_name=None):
        try:
            authenticated = ValidateJson.autenticate_user_with_email(self.payload_batch)
            if authenticated:
                url = config.URL_GITHUB+'/{user_name}'.format(user_name=self.payload_batch['user_name'] )
                response = json.loads(requests.get(url).content)
                authenticated = ValidateJson.validate_user_json(response)
                if authenticated:
                    return response
                return self.return_not_found()
            return self.return_not_found()
        except Exception as ex:
            return self.return_unexpected_error(ex)

class UserRepos(ResourceBase):
    http_methods_allowed = ['GET', 'POST']

    def get(self, user_name=None):
        try:
            authenticated =ValidateJson.autenticate_user_with_email(self.payload_batch)
            if authenticated:
                url = config.URL_GITHUB+'/{user_name}/repos'.format(user_name=self.payload_batch['user_name'] )
                response = json.loads(requests.get(url).content)
                authenticated = ValidateJson.validate_user_json(response)
                if authenticated:
                    return response
                return self.return_not_found()
            return self.return_not_found()
        except Exception as ex:
            return self.return_unexpected_error(ex)

