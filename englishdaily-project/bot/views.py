from telebot import types
from rest_framework.response import Response
from rest_framework.views import APIView

from .bot import bot
from users.views import user_check_instance


class index(APIView):
    def post(self, request):
        """Get messages from TG server and pass them to bot."""

        json_str = request.body.decode("UTF-8")
        # json_to_console(json_str)
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return Response({"code": 200})


@bot.message_handler(commands=["start"])
def start_message(message):
    """Start message. Register user or update username if changed."""

    user_check_instance(message.from_user)

    text = "Wellcome!"

    keyboard = types.InlineKeyboardMarkup()
    key_begin = types.InlineKeyboardButton(
        text="🖊️ begin", callback_data="begin"
    )
    keyboard.add(key_begin)

    bot.send_message(
        message.chat.id, text=text, reply_markup=keyboard, parse_mode="HTML"
    )
