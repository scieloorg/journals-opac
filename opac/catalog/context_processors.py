# coding: utf-8
from django.conf import settings


def access_to_settings(request):
    return {'SETTINGS': settings}
