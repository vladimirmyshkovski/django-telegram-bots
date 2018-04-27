#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_telegram_bots
------------

Tests for `telegram_bots` models module.
"""

# from django.test import TestCase
from test_plus.test import TestCase
from telegram_bots.models import Bot, Authorization
from django.contrib.auth import get_user_model
import mock
from easy_cache import invalidate_cache_key
import telepot

User = get_user_model()


class TestBot(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        telepot.Bot.setWebhook = mock.MagicMock(return_value=True)
        telepot.Bot.getMe = mock.MagicMock(
            return_value={
                'id': 559897142,
                'username': 'global_crypto_signal_bot',
                'first_name': 'Crypto Signals Bot'
            }
        )

    def setUp(self):
        self.bot = Bot.objects.create(
            owner=self.owner,
            api_key="559897142:AAH6v_q2dTuz8tOGcy_MoBrBkGiy9LYtlMc"
        )

    def test_bot_data(self):
        self.assertEqual(self.bot.id, 1)
        self.assertEqual(self.bot.username, "global_crypto_signal_bot")
        self.assertEqual(self.bot.first_name, "Crypto Signals Bot")
        self.assertEqual(self.bot.chat_id, 559897142)

    def test_get_me(self):
        data = {
            'id': 559897142,
            'username': 'global_crypto_signal_bot',
            'first_name': 'Crypto Signals Bot'
        }
        self.assertEqual(
            self.bot.get_me,
            data
        )

    def test_active_auth_user_ids(self):
        user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='password'
        )
        authorization = Authorization.objects.create(
            user=user.telegramuser,
            bot=self.bot,
            is_active=True
        )
        self.assertTrue(authorization.id in self.bot.active_auth_user_ids)

    def test_send_message(self):
        data = {
            'message_id': 12,
            'chat': {
                'username': 'narnikgamarnik',
                'first_name': 'Vladimir',
                'type': 'private',
                'id': 412866215
            },
            'from': {
                'username': 'narnik_bot',
                'first_name': 'Narnik Bot',
                'id': 559897142,
                'is_bot': True
            },
            'date': 1524828220,
            'text': 'hello'
        }
        telepot.Bot.sendMessage = mock.MagicMock(return_value=data)
        answer = self.bot.send_message(chat_id=412866215, payload='hello')
        self.assertEqual(
            answer,
            data
        )

    def test_delete(self):
        telepot.Bot.deleteWebhook = mock.MagicMock(return_value=True)
        self.bot.delete()
        self.assertEqual(
            Bot.objects.filter(pk=1).first(),
            None
        )

    def test_photoes(self):
        invalidate_cache_key('bot_photos:{}'.format(self.bot.id))
        invalidate_cache_key('bot_avatar:{}'.format(self.bot.id))
        data = {
            'photos': [
                [
                    {
                        'width': 160,
                        'file_size': 9011,
                        'height': 160,
                        'file_id': 'AgADAgADsacxG6fWmxhQkeippA4G3' +
                                   'y4VMw4ABLFYff5nuyA2e8QEAAEC'
                    },
                    {
                        'width': 320,
                        'file_size': 26809,
                        'height': 320,
                        'file_id': 'AgADAgADsacxG6fWmxhQkeippA4G3' +
                                   'y4VMw4ABDy7u3imeDbsfMQEAAEC'
                    },
                    {
                        'width': 640,
                        'file_size': 78965,
                        'height': 640,
                        'file_id': 'AgADAgADsacxG6fWmxhQkeippA4G3' +
                                   'y4VMw4ABAGklwOPISe5fcQEAAEC'
                    }
                ]
            ],
            'total_count': 1
        }
        telepot.Bot.getUserProfilePhotos = mock.MagicMock(return_value=data)
        telepot.Bot.getFile = mock.MagicMock(
            return_value={
                "file_path": "photos/file_0.jpg"
            }
        )
        self.assertEqual(
            self.bot.photos,
            [{160: 'https://api.telegram.org/file/bot559897142:' +
                   'AAH6v_q2dTuz8tOGcy_MoBrBkGiy9LYtlMc/photos/file_0.jpg'}]
        )

    def test_photoes_without_data(self):
        telepot.Bot.getUserProfilePhotos = mock.MagicMock(
            return_value={'photos': [], 'total_count': 0}
        )
        invalidate_cache_key('bot_photos:{}'.format(self.bot.id))
        self.assertEqual(
            self.bot.photos,
            []
        )

    def test_avatar(self):
        invalidate_cache_key('bot_photos:{}'.format(self.bot.id))
        invalidate_cache_key('bot_avatar:{}'.format(self.bot.id))
        data = {
            'photos': [
                [
                    {
                        'width': 160,
                        'file_size': 9011,
                        'height': 160,
                        'file_id': 'AgADAgADsacxG6fWmxhQkeippA4G3' +
                                   'y4VMw4ABLFYff5nuyA2e8QEAAEC'
                    },
                    {
                        'width': 320,
                        'file_size': 26809,
                        'height': 320,
                        'file_id': 'AgADAgADsacxG6fWmxhQkeippA4G3' +
                                   'y4VMw4ABDy7u3imeDbsfMQEAAEC'
                    },
                    {
                        'width': 640,
                        'file_size': 78965,
                        'height': 640,
                        'file_id': 'AgADAgADsacxG6fWmxhQkeippA4G3' +
                                   'y4VMw4ABAGklwOPISe5fcQEAAEC'
                    }
                ]
            ],
            'total_count': 1
        }
        telepot.Bot.getUserProfilePhotos = mock.MagicMock(return_value=data)
        telepot.Bot.getFile = mock.MagicMock(
            return_value={
                "file_path": "photos/file_0.jpg"
            }
        )
        self.assertEqual(
            self.bot.avatar,
            'https://api.telegram.org/file/bot559897142:' +
            'AAH6v_q2dTuz8tOGcy_MoBrBkGiy9LYtlMc/photos/file_0.jpg'
        )

    def test_avatar_without_photos(self):
        invalidate_cache_key('bot_photos:{}'.format(self.bot.id))
        invalidate_cache_key('bot_avatar:{}'.format(self.bot.id))
        data = {'photos': [], 'total_count': 0}
        telepot.Bot.getUserProfilePhotos = mock.MagicMock(return_value=data)
        self.assertEqual(
            self.bot.avatar,
            None
        )

    def test_meta(self):
        self.assertEqual(
            self.bot._meta.verbose_name,
            'Bot'
        )
        self.assertEqual(
            self.bot._meta.verbose_name_plural,
            'Bots'
        )

    def test__str__(self):
        self.assertEqual(
            self.bot.__str__(),
            'Crypto Signals Bot'
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.bot.get_absolute_url(),
            '/1/'
        )

    def test_with_exists_pk(self):
        self.bot.save()


class TestTelegramUser(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='password'
        )

    def test_generate_token_len(self):
        token = self.user.telegramuser.generate_token()
        self.assertTrue(len(token) == 64)

    def test_generate_token_string(self):
        token = self.user.telegramuser.generate_token()
        self.assertTrue(isinstance(token, type('')))

    def test_check_token(self):
        token = self.user.telegramuser.token
        self.assertTrue(
            self.user.telegramuser.check_token(token)
        )

    def test_save_with_pk_and_token(self):
        old_token = self.user.telegramuser.token
        self.user.telegramuser.save()
        new_token = self.user.telegramuser.token
        self.assertEqual(
            old_token,
            new_token
        )

    def test_set_token(self):
        old_token = self.user.telegramuser.token
        self.user.telegramuser.set_token()
        new_token = self.user.telegramuser.token
        self.assertNotEqual(
            old_token,
            new_token
        )

    def test__str__(self):
        self.assertEqual(
            self.user.telegramuser.__str__(),
            'testuser2'
        )


class TestAuthorization(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        telepot.Bot.setWebhook = mock.MagicMock(return_value=True)
        telepot.Bot.getMe = mock.MagicMock(
            return_value={
                'id': 559897142,
                'username': 'global_crypto_signal_bot',
                'first_name': 'Crypto Signals Bot'
            }
        )
        self.bot = Bot.objects.create(
            owner=self.owner,
            api_key="559897142:AAH6v_q2dTuz8tOGcy_MoBrBkGiy9LYtlMc"
        )
        self.user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='password'
        )
        self.authorization = Authorization.objects.create(
            user=self.user.telegramuser,
            bot=self.bot,
            is_active=True
        )

    def test_activation_url(self):
        self.assertTrue(
            len(self.authorization.activation_url) > 10
        )

    def test_deactivation_url(self):
        self.assertTrue(
            len(self.authorization.deactivation_url) > 10
        )
