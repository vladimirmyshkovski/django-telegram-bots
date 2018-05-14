from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from .utils import get_telegram_user_model, get_bot_model
from .services import get_user_from_storage, activate_user
from .signals import receive_command

User = get_user_model()
TelegramUser = get_telegram_user_model()
Bot = get_bot_model()


@receiver(post_save, sender=User)
def create_bot_user(sender, instance, created, **kwargs):
    if created:
        TelegramUser.objects.create(user=instance)


@receiver(receive_command, sender=Bot)
def authentication_user(sender, **kwargs):
    if all(k in kwargs for k in ('bot', 'chat_id', 'command', 'payload')):
        command = kwargs['command']
        payload = kwargs['payload']
        bot = kwargs['bot']
        chat_id = kwargs['chat_id']
        #type = kwargs['type']

        if command == 'start':
            if payload:
                user = get_user_from_storage(payload)
                if user:
                    is_activated = activate_user(
                        key=user.id,
                        user=user,
                        bot=bot
                    )
                    if is_activated:
                        reply = 'Hi, {}, the authentication was successful!'.format(
                            user.user.username
                        )
                    else:
                        reply = '{}, you are already authenticated'.format(
                            user.user.username
                        )
                else:
                    reply = 'Unfortunately, I can not authenticate you :('

            else:
                reply = 'You can not be authenticated, \
                since a unique code is not set.'
            if isinstance(bot, Bot):
                bot.send_message(chat_id=chat_id, payload=reply)
