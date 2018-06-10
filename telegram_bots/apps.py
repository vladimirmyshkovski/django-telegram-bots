# -*- coding: utf-8
from django.apps import AppConfig
from django.conf import settings


class TelegramBotsConfig(AppConfig):
    name = 'telegram_bots'
    verbose_name = "TelegramBots"

    def ready(self):
        import telegram_bots.receivers
