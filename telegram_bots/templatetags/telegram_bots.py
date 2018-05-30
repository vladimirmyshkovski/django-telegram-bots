from django import template
from django.contrib.auth import get_user_model
from ..models import Authorization, Bot

User = get_user_model()
register = template.Library()


@register.simple_tag(takes_context=True)
def user_is_subscribed(context, user, bot):
    assert isinstance(user, User), (
        'user must be isinstance of User model'
    )
    assert isinstance(bot, Bot), (
        'bot must be isinstance of Bot model'
    )
    authorization = Authorization.objects.filter(
        user=user.telegramuser,
        bot=bot
    ).first()
    if authorization:
        return True
    return False


@register.inclusion_tag('telegram_bots/button.html')
def subscribe_button(user, bot, button_class, button_text):
    assert isinstance(user, User), (
        'user must be isinstance of User model'
    )
    assert isinstance(bot, Bot), (
        'bot must be isinstance of Bot model'
    )
    authorization, created = Authorization.objects.get_or_create(
        user=user.telegramuser,
        bot=bot
    )
    return {
        'url': authorization.activation_url,
        'button_class': button_class,
        'button_text': button_text
    }


@register.inclusion_tag('telegram_bots/button.html')
def unsubscribe_button(user, bot, button_class, button_text):
    assert isinstance(user, User), (
        'user must be isinstance of User model'
    )
    assert isinstance(bot, Bot), (
        'bot must be isinstance of Bot model'
    )
    authorization, created = Authorization.objects.get_or_create(
        user=user.telegramuser,
        bot=bot
    )
    return {
        'url': authorization.deactivation_url,
        'button_class': button_class,
        'button_text': button_text
    }


@register.inclusion_tag('telegram_bots/button.html')
def toggle_subscribe_button(user, bot, button_class):
    assert isinstance(user, User), (
        'user must be isinstance of User model'
    )
    assert isinstance(bot, Bot), (
        'bot must be isinstance of Bot model'
    )
    authorization, created = Authorization.objects.get_or_create(
        user=user.telegramuser,
        bot=bot
        )
    if authorization.is_active:
        data = {
            'url': authorization.deactivation_url,
            'button_class': button_class,
            'button_text': 'Unsubscribe'
        }
    else:
        data = {
            'url': authorization.activation_url,
            'button_class': button_class,
            'button_text': 'Subscribe'
        }
    return data
