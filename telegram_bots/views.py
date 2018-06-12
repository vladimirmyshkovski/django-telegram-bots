from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404, redirect
from annoying.functions import get_object_or_None
from django.http import HttpResponseBadRequest, JsonResponse
#from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from .utils import (extract_command, decode_signin,
                    get_bot_model, get_telegram_user_model,
                    extract_payload_from_command)
from .services import deactivate_user
from .signals import (subscribed_user, unsubscribed_user, receive_message,
                      receive_callback_query, receive_command, receive_video,
                      receive_document, receive_photo)

from django.views.generic import (View, ListView, CreateView,  # FormView,
                                  DeleteView, DetailView, RedirectView)
#from .forms import MessageForm

import ujson as json


Bot = get_bot_model()
TelegramUser = get_telegram_user_model()


class BotListView(LoginRequiredMixin, ListView):

    model = Bot
    paginate_by = 10
    ordering = ['id']

    def get_queryset(self):
        queryset = super(BotListView, self).get_queryset()
        return queryset.filter(owner=self.request.user)


class BotDetailView(LoginRequiredMixin, DetailView):

    model = Bot


class BotCreateView(LoginRequiredMixin, CreateView):

    model = Bot
    fields = ['api_key']

    def forn_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super(BotCreateView, self).form_valid(form)


class BotDeleteView(LoginRequiredMixin, DeleteView):

    model = Bot


class ReceiveView(View):

    def post(self, request, bot_token):
        bot = get_object_or_None(Bot, api_key=bot_token)
        if bot:  # get_object_or_404(Bot, api_key=bot_token)
            body_unicode = request.body.decode('utf-8')
            payload = json.loads(json.dumps(body_unicode))
            try:
                payload = json.loads(request.body.decode('utf-8'))
            except ValueError:
                return HttpResponseBadRequest('Invalid request body')
            else:
                raw_data = payload
                message = payload.get('message', None)
                callback_query = payload.get('callback_query', None)
                if message:
                    chat_id = payload['message']['chat']['id']
                    if payload['message']['chat']:
                        #type = payload['message']['chat']['type']
                        text = payload['message']['text']  # command
                        message = payload['message']
                        receive_message.send(sender=Bot, bot=bot,
                                             chat_id=chat_id, text=text,
                                             message=message,
                                             raw_data=raw_data)
                    if payload['message']['video']:
                        video = payload['message']['video']
                        receive_video.send(sender=Bot, bot=bot,
                                           chat_id=chat_id, video=video,
                                           raw_data=raw_data)
                    if payload['message']['photo']:
                        photo = payload['message']['photo']
                        receive_photo.send(sender=Bot, bot=bot,
                                           chat_id=chat_id,
                                           photo=photo,
                                           raw_data=raw_data)
                    if payload['message']['document']:
                        document = payload['message']['document']
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
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ReceiveView, self).dispatch(request, *args, **kwargs)


class BotSubscribeView(LoginRequiredMixin, RedirectView):

    def get(self, request, signature):
        data = decode_signin(signature)
        if data:
            user = get_object_or_404(
                TelegramUser, user__username=data['user_username'])
            bot = get_object_or_404(Bot, username=data['bot_username'])
        try:
            subscribed_user.send(
                sender=Bot,
                key=data['key'],
                bot=bot,
                user=user,
            )
            return redirect(
                'https://telegram.me/{}?start={}'.format(bot.username,
                                                         user.token)
                )
        except Exception as e:
            return HttpResponseBadRequest(status=500, reason=e)


class BotUnsubscribeView(LoginRequiredMixin, RedirectView):

    def get(self, request, signature):
        data = decode_signin(signature)
        if data:
            user = get_object_or_404(
                TelegramUser, user__username=data['user_username'])
            bot = get_object_or_404(Bot, username=data['bot_username'])
        try:
            deactivate_user(key=data['key'], user=user, bot=bot)
            unsubscribed_user.send(
                sender=Bot,
                key=data['key'],
                bot=bot,
                user=user,
            )
            return redirect(
                'https://telegram.me/{}?end={}'.format(bot.username,
                                                         user.token)
                )
        except Exception as e:
            return HttpResponseBadRequest(status=500, reason=e)

'''
class BotRefresUserToken(LoginRequiredMixin, RedirectView):

    def get(self, request):

        user = self.request.user
        telegramuser = TelegramUser.objects.filter(user=user)
        if telegramuser:
            telegramuser.set_unique_code
            telegramuser.authorization.is_activate = False
            telegramuser.authorization.save()
            telegramuser.save()

        return super(BotRefresUserToken, self).get(request)
'''

"""
class SendMessageView(LoginRequiredMixin, FormView):
    form_class = MessageForm

    def post(self, request, *args, **kwargs):
        '''
        bot = request.POST.get('bot', None)
        type = request.POST.get('type', None)
        message = request.POST.get('message', None)

        if bot and type and message:
            bot.sendMessage()
        '''
        return super(SendMessageView, self).post(request, *args, **kwargs)
"""
