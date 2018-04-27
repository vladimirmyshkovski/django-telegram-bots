from test_plus.test import TestCase
from django.test import RequestFactory
import mock
import telepot
from telegram_bots.models import Bot, Authorization
from django.contrib.auth import get_user_model
from telegram_bots.signals import (subscribed_user, unsubscribed_user,
                                   activated_user, deactivated_user,
                                   receive_message, receive_command)
import ujson as json
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from django.test import LiveServerTestCase


User = get_user_model()


class TestBotListView(TestCase):

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

    def test_redirect_if_not_logged_in(self):
        resp = self.get('/')
        self.assertRedirects(
            resp,
            '/accounts/login/?next=/',
            fetch_redirect_response=False
        )

    def test_view_url_exists_at_desired_location(self):
        self.login(username='testuser', password='password')
        resp = self.get('/')
        self.response_200(resp)

    def test_view_url_accessible_by_name(self):
        self.login(username='testuser', password='password')
        resp = self.get(
            self.reverse('telegram_bots_list')
        )
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login(username='testuser', password='password')
        resp = self.get(
            self.reverse('telegram_bots_list')
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'telegram_bots/bot_list.html')

    def test_pagination_is_ten(self):
        self.login(username='testuser', password='password')
        resp = self.get(self.reverse('telegram_bots_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)


class TestBotDetailView(TestCase):

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

    def test_redirect_if_not_logged_in(self):
        resp = self.get('/1/')
        self.assertRedirects(
            resp,
            '/accounts/login/?next=/1/',
            fetch_redirect_response=False
        )

    def test_view_url_exists_at_desired_location(self):
        self.login(username='testuser', password='password')
        resp = self.get('/1/')
        self.response_200(resp)

    def test_view_url_accessible_by_name(self):
        self.login(username='testuser', password='password')
        resp = self.get(
            self.reverse('telegram_bots_detail', pk=self.bot.pk)
        )
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login(username='testuser', password='password')
        resp = self.get(
            self.reverse('telegram_bots_detail', pk=self.bot.pk)
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'telegram_bots/bot_detail.html')


class TestBotDeleteView(TestCase):

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

    def test_redirect_if_not_logged_in(self):
        resp = self.get('/1/delete/')
        self.assertRedirects(
            resp,
            '/accounts/login/?next=/1/delete/',
            fetch_redirect_response=False
        )

    def test_view_url_exists_at_desired_location(self):
        self.login(username='testuser', password='password')
        resp = self.get('/1/delete/')
        self.response_200(resp)

    def test_view_url_accessible_by_name(self):
        self.login(username='testuser', password='password')
        resp = self.get(
            self.reverse('telegram_bots_delete', pk=self.bot.pk)
        )
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login(username='testuser', password='password')
        resp = self.get(
            self.reverse('telegram_bots_delete', pk=self.bot.pk)
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'telegram_bots/bot_confirm_delete.html')


class TestBotSubscribeView(TestCase):
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
            password='password2'
        )
        self.authorization = Authorization.objects.create(
            user=self.user.telegramuser,
            bot=self.bot
        )

    def test_redirect(self):
        self.client.login(username='testuser2', password='password2')
        resp = self.get(self.authorization.activation_url)
        self.assertRedirects(
            resp,
            'https://telegram.me/{}?start={}'.format(
                self.bot.username,
                self.user.telegramuser.token
            ),
            fetch_redirect_response=False
        )
    '''
    def test_activate_user(self):
        self.client.login(username='testuser2', password='password2')
        self.get(self.authorization.activation_url)
        authorization = Authorization.objects.get(
            user=self.user.telegramuser,
            bot=self.bot
        )
        self.assertTrue(authorization.is_active)

    def test_send_activated_user_signal(self):
        self.client.login(username='testuser2', password='password2')
        self.signal_was_called = False
        self.key = None

        def handler(sender, key, **kwargs):
            self.signal_was_called = True
            self.key = key

        activated_user.connect(handler)

        self.get(self.authorization.activation_url)
        self.assertEqual(
            self.key,
            self.authorization.pk
        )
        self.assertTrue(self.signal_was_called)
        activated_user.disconnect(handler)
    '''

    def test_send_subscribed_user_signal(self):
        self.client.login(username='testuser2', password='password2')
        self.signal_was_called = False
        self.key = None

        def handler(sender, key, **kwargs):
            self.signal_was_called = True
            self.key = key

        subscribed_user.connect(handler)

        self.get(self.authorization.activation_url)
        self.assertEqual(
            self.key,
            self.authorization.pk
        )
        self.assertTrue(self.signal_was_called)
        subscribed_user.disconnect(handler)

    def test_with_invalid_signature(self):
        self.client.login(username='testuser2', password='password2')
        resp = self.get('/subscribe/fakesignature/')
        self.assertEqual(resp.status_code, 500)


class TestBotUnsubscribeView(TestCase):
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
            password='password2'
        )
        self.authorization = Authorization.objects.create(
            user=self.user.telegramuser,
            bot=self.bot,
            is_active=True
        )

    def test_redirect(self):
        self.client.login(username='testuser2', password='password2')
        resp = self.get(self.authorization.activation_url)
        self.assertRedirects(
            resp,
            'https://telegram.me/{}?start={}'.format(
                self.bot.username,
                self.user.telegramuser.token
            ),
            fetch_redirect_response=False
        )

    def test_deactivate_user(self):
        self.client.login(username='testuser2', password='password2')
        self.get(self.authorization.deactivation_url)
        authorization = Authorization.objects.get(
            user=self.user.telegramuser,
            bot=self.bot,
        )
        self.assertFalse(authorization.is_active)

    def test_send_deactivated_user_signal(self):
        self.client.login(username='testuser2', password='password2')
        self.signal_was_called = False
        self.key = None

        def handler(sender, key, **kwargs):
            self.signal_was_called = True
            self.key = key

        deactivated_user.connect(handler)

        self.get(self.authorization.deactivation_url)
        self.assertEqual(
            self.key,
            self.authorization.pk
        )
        self.assertTrue(self.signal_was_called)
        deactivated_user.disconnect(handler)

    def test_send_unsubscribed_user_signal(self):
        self.client.login(username='testuser2', password='password2')
        self.signal_was_called = False
        self.key = None

        def handler(sender, key, **kwargs):
            self.signal_was_called = True
            self.key = key

        unsubscribed_user.connect(handler)

        self.get(self.authorization.deactivation_url)
        self.assertEqual(
            self.key,
            self.authorization.pk
        )
        self.assertTrue(self.signal_was_called)
        unsubscribed_user.disconnect(handler)

    def test_with_invalid_signature(self):
        self.client.login(username='testuser2', password='password2')
        resp = self.get('/unsubscribe/fakesignature/')
        self.assertEqual(resp.status_code, 500)


class TestReceiverView(TestCase):

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
            password='password2'
        )

        self.message = [
            {
                'message': {
                    'chat': {
                        'type': 'private',
                        'first_name': 'Vladimir',
                        'username': 'narnikgamarnik',
                        'id': 412866215
                    },
                    'message_id': 13,
                    'text': 'фывфыв',
                    'date': 1524857311,
                    'from': {
                        'language_code': 'en-US',
                        'is_bot': False,
                        'username': 'narnikgamarnik',
                        'first_name': 'Vladimir',
                        'id': 412866215
                    }
                },
                'update_id': 330953614
            },
            {
                'message': {
                    'chat': {
                        'type': 'private',
                        'first_name': 'Vladimir',
                        'username': 'narnikgamarnik',
                        'id': 412866215
                    },
                    'from': {
                        'language_code': 'en-US',
                        'is_bot': False,
                        'username': 'narnikgamarnik',
                        'first_name': 'Vladimir',
                        'id': 412866215
                    },
                    'entities': [
                        {
                            'offset': 0,
                            'length': 6,
                            'type': 'bot_command'
                        }
                    ],
                    'date': 1524862011,
                    'message_id': 14,
                    'text': '/start'
                },
                'update_id': 330953615
            },
            {
                'message': {
                    'chat': {
                        'type': 'private',
                        'first_name': 'Vladimir',
                        'username': 'narnikgamarnik',
                        'id': 412866215
                    },
                    'from': {
                        'language_code': 'en-US',
                        'is_bot': False,
                        'username': 'narnikgamarnik',
                        'first_name': 'Vladimir',
                        'id': 412866215
                    },
                    'entities': [
                        {
                            'offset': 0,
                            'length': 6,
                            'type': 'bot_command'
                        }
                    ],
                    'date': 1524862021,
                    'message_id': 15,
                    'text': "/start hello"
                },
                'update_id': 330953616
            }
        ]
        self.dump_message = json.dumps(self.message[0])

    def test_with_valid_data(self):
        resp = self.client.generic(
            'POST',
            '/{}/'.format(self.bot.api_key),
            self.dump_message
        )
        self.response_200(resp)

    def test_send_message_signal(self):
        self.signal_was_called = False
        self.signal_bot = None
        self.signal_chat_id = None
        self.signal_text = None
        self.signal_message = None

        def handler(sender, bot, chat_id, text, message, **kwargs):
            self.signal_was_called = True
            self.signal_bot = bot
            self.signal_chat_id = chat_id
            self.signal_text = text
            self.signal_message = message

        receive_message.connect(handler)
        resp = self.client.generic(
            'POST',
            '/{}/'.format(self.bot.api_key),
            self.dump_message
        )
        self.response_200(resp)
        self.assertTrue(self.signal_was_called)
        self.assertEqual(
            self.signal_bot,
            self.bot
        )
        self.assertEqual(
            self.signal_chat_id,
            412866215
        )
        self.assertEqual(
            self.signal_text,
            'фывфыв'
        )
        self.assertEqual(
            self.signal_message,
            self.message[0]['message']
        )
        receive_message.disconnect(handler)

    def test_send_command_signal_without_payload(self):
        message = json.dumps(self.message[1])
        self.signal_was_called = False
        self.signal_bot = None
        self.signal_chat_id = None
        self.signal_command = None
        self.signal_payload = None

        def handler(sender, bot, chat_id, command, payload, **kwargs):
            self.signal_was_called = True
            self.signal_bot = bot
            self.signal_chat_id = chat_id
            self.signal_command = command
            self.signal_payload = payload

        receive_command.connect(handler)

        resp = self.client.post('/{}/'.format(self.bot.api_key),
                                message,
                                content_type="application/json")
        self.response_200(resp)
        self.assertTrue(self.signal_was_called)
        self.assertEqual(
            self.signal_bot,
            self.bot
        )
        self.assertEqual(
            self.signal_chat_id,
            412866215
        )
        self.assertEqual(
            self.signal_command,
            'start'
        )
        self.assertEqual(
            self.signal_payload,
            ''
        )
        receive_command.disconnect(handler)

    def test_send_command_signal_with_payload(self):
        message = json.dumps(self.message[2])
        self.signal_was_called = False
        self.signal_bot = None
        self.signal_chat_id = None
        self.signal_command = None
        self.signal_payload = None

        def handler(sender, bot, chat_id, command, payload, **kwargs):
            self.signal_was_called = True
            self.signal_bot = bot
            self.signal_chat_id = chat_id
            self.signal_command = command
            self.signal_payload = payload

        receive_command.connect(handler)

        resp = self.client.post('/{}/'.format(self.bot.api_key),
                                message,
                                content_type="application/json")
        self.response_200(resp)
        self.assertTrue(self.signal_was_called)
        self.assertEqual(
            self.signal_bot,
            self.bot
        )
        self.assertEqual(
            self.signal_chat_id,
            412866215
        )
        self.assertEqual(
            self.signal_command,
            'start'
        )
        self.assertEqual(
            self.signal_payload,
            'hello'
        )
        receive_command.disconnect(handler)

'''
class TestBotListSelenium(LiveServerTestCase):

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
        self.selenium = webdriver.Firefox()
        super(TestBotListSelenium, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(TestBotListSelenium, self).tearDown()

    def test_template(self):
        selenium = self.selenium
        self.client.login(username='testuser', password='password')
        print(self.live_server_url````````)
        #selenium.get("%s" % (self.live_server_url))
        import time
        time.sleep(10)
        print('hello')
'''
