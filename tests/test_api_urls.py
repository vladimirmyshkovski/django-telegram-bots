#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_telegram_bots
------------

Tests for `telegram_bots` models module.
"""

#from django.test import TestCase
from test_plus.test import TestCase
from rest_framework.test import APIRequestFactory, RequestsClient
from telegram_bots.models import Bot, TelegramUser
from django.contrib.auth import get_user_model
import mock
import string
import random

import telepot
import ujson as json

class TestBotUrls(TestCase):
	
	def setUp(self):
		self.factory = APIRequestFactory()
		owner = self.make_user()
		Bot.objects.create(owner=owner, api_key="559897142:AAH6v_q2dTuz8tOGcy_MoBrBkGiy9LYtlMc")

	def testUrls(self):
		client = RequestsClient()
		response = client.get('http://127.0.0.1:8000/api/bots/')
		data = json.loads('{"first_name":"Narnik Bot","username":"narnik_bot","avatar":null}')
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(json.loads(response.content.decode('utf-8'))[0], data)