from bot.bot import bot
from bot.controller import get_tg_page
from bot.keyboards.main import kb_main
from users.controller import user_check_instance


def start_message(message):
    """Start message. Register user or update username if changed."""

    user_check_instance(message.from_user)

    text = get_tg_page("start")

    # keyboard = types.InlineKeyboardMarkup()
    # key_begin = types.InlineKeyboardButton(
    #     text="🖊️ begin", callback_data="begin"
    # )
    # keyboard.add(key_begin)

    bot.send_message(
        message.chat.id, text=text, reply_markup=kb_main, parse_mode="HTML"
    )


def help_message(message):
    """Help message. Commans list."""

    text = get_tg_page("help")
    bot.send_message(
        message.chat.id, text=text, reply_markup=kb_main, parse_mode="HTML"
    )


def register_hendlers_common():
    bot.register_message_handler(start_message, commands=["start"])
    bot.register_message_handler(help_message, commands=["help"])
