from telegram_bots.models import Bot
from telegram_bots.utils import extract_command, extract_payload_from_command
from telegram_bots.signals import (receive_command, receive_message,
                                   receive_callback_query, receive_video,
                                   receive_document, receive_photo)

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
                if update['message']['chat']:
                    #type = update['message']['chat']['type']
                    text = update['message']['text']  # command
                    message = update['message']
                    receive_message.send(sender=Bot, bot=bot,
                                         chat_id=chat_id, text=text,
                                         message=message,
                                         raw_data=raw_data)
                elif update['message']['video']:
                    video = update['message']['video']
                    receive_video.send(sender=Bot, bot=bot,
                                       chat_id=chat_id, video=video,
                                       raw_data=raw_data)
                elif update['message']['photo']:
                    photo = update['message']['photo']
                    receive_photo.send(sender=Bot, bot=bot,
                                       chat_id=chat_id,
                                       photo=photo,
                                       raw_data=raw_data)
                elif update['message']['document']:
                    document = update['message']['document']
                    receive_document.send(sender=Bot, bot=bot,
                                          chat_id=chat_id,
                                          document=document,
                                          raw_data=raw_data)
                command = extract_command(text)
                if command:
                    payload = extract_payload_from_command(text)
                    receive_command.send(
                        sender=Bot, bot=bot, chat_id=chat_id,
                        command=command, payload=payload,
                        raw_data=raw_data
                    )
            if callback_query:
                receive_callback_query.send(
                    sender=Bot, bot=bot,
                    chat_id=callback_query['from']['id'],
                    data=callback_query['data'],
                    raw_data=raw_data
                )
