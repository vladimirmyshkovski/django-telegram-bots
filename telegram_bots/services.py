from annoying.functions import get_object_or_None
from .utils import (get_authorization_model,
                    get_telegram_user_model,
                    get_bot_model)


User = get_telegram_user_model()
Authorization = get_authorization_model()
Bot = get_bot_model()


def get_user_from_storage(token):
    user = get_object_or_None(User, token=token)
    return user


def activate_user(key, user, bot):
    from .signals import activated_user

    assert isinstance(user, User), (
        'user must be isinstance of TelegramUser model'
    )
    assert isinstance(bot, Bot), (
        'bot must be isinstance of Bot model'
    )

    authorization, created = Authorization.objects.get_or_create(bot=bot,
                                                                 user=user)
    if not authorization.is_active:
        authorization.is_active = True
        authorization.save()
        activated_user.send(sender=Bot, key=key, user=user, bot=bot)
        return True
    return False


def deactivate_user(key, user, bot):
    from .signals import deactivated_user

    assert isinstance(user, User), (
        'user must be isinstance of TelegramUser model'
    )
    assert isinstance(bot, Bot), (
        'bot must be isinstance of Bot model'
    )
    authorization, created = Authorization.objects.get_or_create(bot=bot,
                                                                 user=user)
    if authorization.is_active:
        authorization.is_active = False
        authorization.save()
        deactivated_user.send(sender=Bot, key=key, user=user, bot=bot)
        return True
    return False
'''
def save_chat_id(chat_id, user):
    telegram_user, created = User.objects.get_or_create(user)
    #chat, created = Chat.objects.get_or_create(chat_id=chat_id)
    #chat.type = type
    telegram_user.chat_id = chat_id
    chat.save()
    return chat
'''
