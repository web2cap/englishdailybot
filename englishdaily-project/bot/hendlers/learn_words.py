import logging

# from random import randint

# from telebot import custom_filters
from telebot.types import CallbackQuery
from telebot.callback_data import CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

from bot.bot import bot
from bot.controller import get_tg_page

# from bot.factories.wordlist_factory import wordlist_factory
# from bot.keyboards.native_wordlists import products_keyboard
from bot.keyboards.main import kb_main

# from bot.states.follow_wordlist import FollowWordlistState
from words.controller import learn_words_hello


def learn_words_start(message):
    """Learn words hello message."""

    subscriptions = learn_words_hello()
    if subscriptions and subscriptions.count():
        text = "Daily plan:\n"
        for s in subscriptions:
            text += f"{s.list}: {s.rate} words\n"

        text = "Let's begin? /learn_begin"

    bot.send_message(
        message.chat.id,
        text=text,
    )


def register_hendlers_learn_words():

    bot.register_message_handler(learn_words_start, commands=["learn"])
