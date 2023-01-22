from bot.bot import bot
from bot.controller import get_tg_page
from bot.keyboards.native_wordlists import kb_native_wordlists


def wordlist_message(message):
    """Start wordlist message. Choose the list for practice."""

    text = get_tg_page("wordlist")

    bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=kb_native_wordlists,
        parse_mode="HTML",
    )


def register_hendlers_word():
    bot.register_message_handler(wordlist_message, commands=["wordlist"])
