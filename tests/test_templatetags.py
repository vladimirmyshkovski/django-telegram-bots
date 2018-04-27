from test_plus.test import TestCase
from django.test import RequestFactory
import mock
import telepot
from django.contrib.auth import get_user_model
from telegram_bots.models import Bot, Authorization
from django.template import Context, Template


User = get_user_model()


class TestSubscribeButton(TestCase):

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
        self.request_factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='password'
        )

    def test_with_valid_data(self):

        request = self.request_factory.get('/?ref=123123123')
        request.user = self.user

        out = Template(
            "{% load telegram_bots_tags %}"
            "{% subscribe_button button_class='btn btn-primary' button_text='Subscribe' bot=bot user=user %}"
        ).render(Context({
            'request': request,
            'user': self.user,
            'bot': self.bot
            })
        )
        authorization = Authorization.objects.get(
            user=self.user.telegramuser,
            bot=self.bot
        )
        self.assertEqual(
            out,
            '<a href="/subscribe/{}/" class="{}">{}</a>'.format(
                authorization.activation_url.split('/')[2],
                'btn btn-primary',
                'Subscribe'
                )
            )


class TestUnsubscribeButton(TestCase):

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
        self.request_factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='password'
        )

    def test_with_valid_data(self):

        request = self.request_factory.get('/?ref=123123123')
        request.user = self.user

        out = Template(
            "{% load telegram_bots_tags %}"
            "{% unsubscribe_button button_class='btn btn-primary' button_text='Unsubscribe' bot=bot user=user %}"
        ).render(Context({
            'request': request,
            'user': self.user,
            'bot': self.bot
            })
        )
        authorization = Authorization.objects.get(
            user=self.user.telegramuser,
            bot=self.bot
        )
        self.assertEqual(
            out,
            '<a href="/unsubscribe/{}/" class="{}">{}</a>'.format(
                authorization.deactivation_url.split('/')[2],
                'btn btn-primary',
                'Unsubscribe'
                )
            )