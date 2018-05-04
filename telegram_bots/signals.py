from django.dispatch import Signal


receive_message = Signal(providing_args=['bot', 'chat_id', 'text', 'message'])

receive_command = Signal(providing_args=['bot', 'chat_id', 'command',
                                         'payload'])

receive_callback_query = Signal(providing_args=['bot_id', 'chat_id', 'data'])

subscribed_user = Signal(providing_args=['key', 'user', 'bot'])
unsubscribed_user = Signal(providing_args=['key', 'user', 'bot'])

activated_user = Signal(providing_args=['key', 'user', 'bot'])
deactivated_user = Signal(providing_args=['key', 'user', 'bot'])
