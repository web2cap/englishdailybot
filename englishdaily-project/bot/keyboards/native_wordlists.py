from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.factories.wordlist_factory import wordlist_factory
from words.controller import get_word_lists


def products_keyboard():
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text=list.name,
                    callback_data=wordlist_factory.new(id=list.id),
                )
            ]
            for list in get_word_lists()
        ]
    )
