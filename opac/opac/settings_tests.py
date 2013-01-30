# coding: utf-8
"""
This module is used by the test runner.
"""
import os


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

execfile(os.path.join(PROJECT_PATH, 'settings.py'))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db_test.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '',
    }
}
