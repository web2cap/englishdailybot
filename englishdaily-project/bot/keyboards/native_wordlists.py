from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from words.controller import get_word_lists


kb_native_wordlists = InlineKeyboardMarkup()

for list in get_word_lists():
    text = list.name
    if list.name_translated:
        text += f" ({list.name_translated})"
    kb_native_wordlists.add(
        InlineKeyboardButton(text=text, callback_data=list.id)
    )
