from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.factories.wordlist import factory_wordlist
from words.controller import get_word_lists


def kb_wordlist():
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text=list.name,
                    callback_data=factory_wordlist.new(id=list.id),
                )
            ]
            for list in get_word_lists()
        ]
    )
