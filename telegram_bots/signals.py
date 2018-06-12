from django.dispatch import Signal


receive_message = Signal(providing_args=['bot', 'chat_id', 'text', 'message',
                                         'raw_data'])

receive_video = Signal(providing_args=['bot', 'chat_id', 'video', 'message',
                                       'raw_data'])

receive_document = Signal(providing_args=['bot', 'chat_id', 'document',
                                          'raw_data'])

receive_photo = Signal(providing_args=['bot', 'chat_id', 'photo', 'raw_data'])

receive_command = Signal(providing_args=['bot', 'chat_id', 'command',
                                         'payload', 'raw_data'])

receive_callback_query = Signal(providing_args=['bot', 'chat_id', 'data',
                                                'raw_data'])

subscribed_user = Signal(providing_args=['key', 'user', 'bot'])
unsubscribed_user = Signal(providing_args=['key', 'user', 'bot'])

activated_user = Signal(providing_args=['key', 'user', 'bot'])
deactivated_user = Signal(providing_args=['key', 'user', 'bot'])
