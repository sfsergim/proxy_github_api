#  -*- coding: utf-8 -*-
"""
Config File for enviroment variables
"""
from __future__ import unicode_literals
import os
from importlib import import_module


class Config(object):
    """
    Base class for all config variables
    """
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    AMBIENTE = None

    def __init__(self):
        if self.AMBIENTE is None:
            raise TypeError('You should use one of the specialized config class')
        self.APP_URL = os.environ['APP_URL']
        self.URL_GITHUB = os.environ['GITHUB_URL']

class DevelopmentConfig(Config):
    """
    Development Config... this is your home developer!
    """
    AMBIENTE = 'development'
    DEVELOPMENT = True
    DEBUG = True

class ConfigClassNotFound(Exception):
    """
    Raises when the APP_SETTINGS environment variable have a value which does not point to an uninstantiable class.
    """
    pass


def get_config():
    """
    Get the Config Class instance defined in APP_SETTINGS environment variable
    :return The config class instance
    :rtype: Config
    """
    config_imports = os.environ['APP_SETTINGS'].split('.')
    config_class_name = config_imports[-1]
    config_module = import_module('.'.join(config_imports[:-1]))
    config_class = getattr(config_module, config_class_name, True)
    
    if not config_class:
        raise ConfigClassNotFound('Unable to find a config class in {}'.format(os.environ['APP_SETTINGS']))
    return config_class()