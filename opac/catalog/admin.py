# -*- coding: utf-8 -*-
from django.contrib import admin

from . import models


admin.site.register(models.CollectionMeta)
admin.site.register(models.JournalMeta)
