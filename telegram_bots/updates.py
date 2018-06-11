from telegram_bots.models import Bot
from telegram_bots.utils import extract_command, extract_payload_from_command
from telegram_bots.signals import (receive_command, receive_message,
                                   receive_callback_query)


from django.core.cache import cache


def get_updates():
    bots = Bot.objects.all()
    for bot in bots:
        last_update = cache.get('last_update_{}'.format(bot.chat_id), None)
        updates = bot.bot.getUpdates(offset=last_update)
        for update in updates:
            raw_data = update
            if not last_update:
                last_update = update['update_id']
                cache.set(
                    'last_update_{}'.format(bot.chat_id), update['update_id']
                )
            last_update += 1
            cache.set('last_update_{}'.format(bot.chat_id), last_update)

            message = update.get('message', None)
            callback_query = update.get('callback_query', None)
            if message:
                chat_id = update['message']['chat']['id']
                #type = update['message']['chat']['type']
                text = update['message']['text']  # command
                message = update['message']
                command = extract_command(text)
                if command:
                    payload = extract_payload_from_command(text)
                    receive_command.send(
                        sender=Bot, bot=bot, chat_id=chat_id,
                        command=command, payload=payload,
                        raw_data=raw_data
                    )
                else:
                    receive_message.send(sender=Bot, bot=bot,
                                         chat_id=chat_id, text=text,
                                         message=message,
                                         raw_data=raw_data)
            if callback_query:
                receive_callback_query.send(
                    sender=Bot, bot=bot,
                    user_id=callback_query['from']['id'],
                    data=callback_query['data'],
                    raw_data=raw_data
                )
