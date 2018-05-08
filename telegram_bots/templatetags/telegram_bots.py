from django import template
from ..models import Authorization

register = template.Library()


@register.inclusion_tag('telegram_bots/button.html')
def subscribe_button(user, bot, button_class, button_text):
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
