from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot import types

from .bot import bot

from .hendlers.comon import register_hendlers_common
from .hendlers.wordlist import register_hendlers_wordlist

# from .hendlers.learn_words import register_hendlers_learn_words


class index(APIView):
    def post(self, request):
        """Get messages from TG server and pass them to bot."""

        json_str = request.body.decode("UTF-8")
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])
        self.register_all_hendlers()
        return Response({"code": 200})

    def register_all_hendlers(self):
        """Register all hendlers from message handlers functions."""

        register_hendlers_common()
        register_hendlers_wordlist()
        # register_hendlers_learn_words()
