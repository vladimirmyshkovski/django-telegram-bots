#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_telegram_bots
------------

Tests for `telegram_bots` models module.
"""

#from django.test import TestCase
from test_plus.test import TestCase

from telegram_bots.models import Bot, TelegramUser, Authorization
from django.contrib.auth import get_user_model
import mock
import string
import random

import telepot


class TestBot(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		User = get_user_model()
		owner = User.objects.create(username='testuser', email='testuser@example.com', password='password')
		cls.bot = Bot.objects.create(owner=owner, api_key="559897142:AAH6v_q2dTuz8tOGcy_MoBrBkGiy9LYtlMc")

	def setUp(self):
		pass
		#owner = self.make_user()
		#Bot.objects.create(owner=owner, api_key="559897142:AAH6v_q2dTuz8tOGcy_MoBrBkGiy9LYtlMc")

	def test_bot_data(self):
		self.assertEqual(self.bot.id, 1)
		self.assertEqual(self.bot.username, "narnik_bot")
		self.assertEqual(self.bot.first_name, "Narnik Bot")
		self.assertEqual(self.bot.chat_id, 559897142)
	
	def fake_get_me(self):
		data = {}
		data['id'] = 559897142
		data['is_bot'] = True
		data['first_name'] = 'Narnik Bot'
		data['username'] = 'narnik_bot'
		return data

	def fake_send_message(self, chat_id='412866215', payload='hello world'):
		message = {'chat': {'id': chat_id, 'first_name': 'Vladimir', 'type': 'private', 'username': 'narnikgamarnik'}, 'date': 1522148609, 'from': {'id': 559897142, 'first_name': 'Narnik Bot', 'is_bot': True, 'username': 'narnik_bot'}, 'text': payload, 'message_id': 11}
		return message

	@mock.patch('telegram_bots.models.Bot.get_me', fake_get_me)
	def test_fake_get_me(self):
		data = {'id': 559897142, 'is_bot': True, 'first_name': 'Narnik Bot', 'username': 'narnik_bot'}
		return self.assertEqual(self.fake_get_me(), data)
	
	@mock.patch('telegram_bots.models.Bot.send_message', fake_send_message)
	def test_send_message(self, chat_id='412866215', payload='hello world'):
		message = {'chat': {'id': chat_id, 'first_name': 'Vladimir', 'type': 'private', 'username': 'narnikgamarnik'}, 'date': 1522148609, 'from': {'id': 559897142, 'first_name': 'Narnik Bot', 'is_bot': True, 'username': 'narnik_bot'}, 'text': payload, 'message_id': 11}
		return self.assertEqual(self.fake_send_message(), message)


class TestTelegramUser(TestCase):

	@classmethod
	def setUpTestData(cls):
		#Set up non-modified objects used by all test methods
		#Author.objects.create(first_name='Big', last_name='Bob')
		#user = TestCase.make_user()
		User = get_user_model()
		cls.user = User.objects.create(username='testuser', email='testuser@example.com', password='password')
		cls.telegramuser = TelegramUser.objects.first()

	def setUp(self):
		pass

	def test_creation_telegramuser(self):
		telegramuser = TelegramUser.objects.get(user=self.user)
		self.assertEquals(telegramuser, self.user.telegramuser)
		self.telegramuser = telegramuser

	def test_user_label(self):
		field_label = self.telegramuser._meta.get_field('user').verbose_name
		self.assertEquals(field_label,'User')

	def test_token_label(self):
		field_label = self.telegramuser._meta.get_field('token').verbose_name
		self.assertEquals(field_label,'Token')

	def test_chat_id_label(self):
		field_label = self.telegramuser._meta.get_field('chat_id').verbose_name
		self.assertEquals(field_label,'Chat id')

	def test_telegramuser_data(self):
		token = self.telegramuser.token
		self.assertTrue(self.telegramuser.check_token(token), True)
		self.assertEqual(self.telegramuser.chat_id, None)
		self.assertEqual(self.telegramuser.user.username, 'testuser')

	def test_telegramuser_check_token(self):
		token = self.telegramuser.token
		self.assertTrue(self.telegramuser.check_token(token))

	def fake_generate_token(self, size=64, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
		token = ''.join(random.choice(chars) for _ in range(size))
		return token

	def test_fake_generate_token(self):
		return self.assertNotEqual(self.fake_generate_token, self.telegramuser.token)

	def test_set_token(self):
		token = self.fake_generate_token()
		self.telegramuser.token = token
		return self.assertEqual(self.telegramuser.token, token)


class TestAuthorization(TestCase):

	@classmethod
	def setUpTestData(cls):
		User = get_user_model()
		owner = User.objects.create(username='owner', email='owner@example.com', password='password')
		cls.bot = Bot.objects.create(owner=owner, api_key="559897142:AAH6v_q2dTuz8tOGcy_MoBrBkGiy9LYtlMc")
		cls.user_one = User.objects.create(username='testuser_one', email='testuser_one@example.com', password='password')
		cls.user_two = User.objects.create(username='testuser_two', email='testuser_two@example.com', password='password')
		cls.authorization = Authorization.objects.create(bot=cls.bot, user=cls.user_one.telegramuser)

	def setUp(self):
		pass

	def test_bot_label(self):
		field_label = self.authorization._meta.get_field('bot').verbose_name
		self.assertEquals(field_label,'Bot')

	def test_bot_related_name(self):
		related_name = self.bot._meta.get_field('authorizations').related_name
		self.assertEquals(related_name,'authorizations')

	def test_user_label(self):
		field_label = self.authorization._meta.get_field('user').verbose_name
		self.assertEquals(field_label,'User')

	def test_user_related_name(self):
		related_name = self.authorization.user._meta.get_field('authorizations').related_name
		self.assertEquals(related_name,'authorizations')		