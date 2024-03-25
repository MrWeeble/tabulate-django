# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

INSTALLED_APPS = ("test_app",)

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

SECRET_KEY = "something"
