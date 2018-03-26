# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from telegram_bots.urls import urlpatterns as telegram_bots_urls

urlpatterns = [
    url(r'^', include(telegram_bots_urls)),
]
