# -*- coding: utf-8 -*-

"""
This module define all the api endpoints
"""
from flask import Flask
from flask_restful import Api


def create_api(app):
    """
    Used when creating a Flask App to register the REST API and its resources
    """
    from app.presentation import resources
    api = Api(app)
  
    api.add_resource(resources.UserLoginResource, '/api/github/user/login/<user_name>')
    api.add_resource(resources.Users, '/api/github/users/since')
    api.add_resource(resources.UserDetails, '/api/github/users/<string:user_name>/details')
    api.add_resource(resources.UserRepos,   '/api/github/users/<string:user_name>/repos')
